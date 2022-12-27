import json
from django.apps.registry import apps
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from streamer.serializers import SelfStreamerSerializer
from .serializers import UserServiceSerializer
from .models import Service, UserService
from datetime import datetime
import requests

GROUP_NAME_GENERAL_NOTIFICATIONS = "notif_general"
GROUP_NAME_STAFF_NOTIFICATIONS = "notif_staff"
GROUP_NAME_TWITCH_EVENTSUB = "twitch_eventsub"


class ServiceConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self._msg_class_map = {
            "vue.logout": self._handle__vue_logout,
            "vue.cb.render.sidebar": self._handle__vue_cb_render_sidebar,
            "vue.cb.route.push": self._handle__vue_cb_route_push,
            "vue.get.users.services.status": self._handle__vue_cb_users_services_status,
            "vue.verify.users.services": self._handle__vue_cb_verify_users_services,
            "vue.users.services.oauth.flow": self._handle__vue_cb_users_services_oauth_flow,
        }
        self._allowed_groups = []
        super().__init__(*args, **kwargs)

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        msg_class = json_data.get("class", "unknown")
        try:
            await self._msg_class_map[msg_class](json_data)

        except (IndexError, KeyError) as e:
            await self.send(
                text_data=json.dumps(
                    {
                        "class": "sb.error",
                        "message": "Failed to interpret sent message type.",
                    }
                )
            )

    @database_sync_to_async
    def get_self_user_serializer(self):
        return SelfStreamerSerializer(self.scope["user"]).data

    @database_sync_to_async
    def update_user_service_verify_time(self, service_name):
        user = self.scope["user"]
        try:
            service = Service.objects.get(name=service_name)
            userservice = UserService.objects.get(
                user_id=user.id, service_id=service.id
            )
        except (Service.DoesNotExist, UserService.DoesNotExist):
            return

        userservice.last_verified = datetime.utcnow()
        userservice.save()

        return userservice.last_verified

    @database_sync_to_async
    def get_service(self, name):
        try:
            service = Service.objects.prefetch_related("userservice_set").get(name=name)
        except (Service.DoesNotExist):
            return None

        return service

    @database_sync_to_async
    def get_user_service(self, name):
        user = self.scope["user"]
        try:
            service = Service.objects.get(name=name)
            userservice = UserService.objects.prefetch_related("service", "user").get(
                user_id=user.id, service_id=service.id
            )
        except (Service.DoesNotExist, UserService.DoesNotExist):
            return None

        return userservice

    @database_sync_to_async
    def get_user_service_serializer(self, name):
        user = self.scope["user"]
        try:
            service = Service.objects.get(name=name)
            queryset = UserService.objects.get(user_id=user.id, service_id=service.id)
        except (Service.DoesNotExist, UserService.DoesNotExist):
            return {}

        return UserServiceSerializer(queryset).data

    async def connect(self):
        if self.scope["user"].is_authenticated:
            await self.accept("jwt_bearer")
            serialized_output = await self.get_self_user_serializer()

            self._allowed_groups.append(GROUP_NAME_GENERAL_NOTIFICATIONS)
            if self.scope["user"].is_staff:
                self._allowed_groups.append(GROUP_NAME_STAFF_NOTIFICATIONS)

            for group_name in self._allowed_groups:
                # Auto subscribe to the right groups for the user level
                await self.channel_layer.group_add(group_name, self.channel_name)

            await self.send(
                text_data=json.dumps(
                    {
                        "class": "sb.users.self",
                        "data": serialized_output,
                    }
                )
            )
        else:
            await self.disconnect(403)

    async def disconnect(self, close_code):
        for group_name in self.groups:
            await self.channel_layer.group_discard(group_name, self.channel_name)
        self._allowed_groups = []
        await self.close(close_code)

    async def _handle__vue_logout(self, json_data={}):
        await self.send(
            text_data=json.dumps(
                {"class": "sb.logout", "message": "Disconnecting by user request."}
            )
        )
        self.disconnect(200)

    async def _handle__vue_cb_route_push(self, json_data={}):
        pass
        # await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def _handle__vue_cb_render_sidebar(self, json_data={}):
        pass

    async def _handle__vue_cb_users_services_status(self, json_data={}):
        user = self.scope["user"]
        service_name = json_data["service"]
        service: Service = await self.get_service(name=service_name)

        if not service:
            await self.send(
                text_data=json.dumps(
                    {
                        "class": "sb.error",
                        "message": "Missing service configuration for {}".format(
                            service_name
                        ),
                    }
                )
            )
            return

        data = {
            "oauth_url": service.oauth_login_url,
            "client_id": service.api_client_id,
            "request_scopes": service.broad_scope.split(" "),
            "linked": False,
            "verified": False,
            "scopes": [],
            "identity": "",
        }

        for user_service in service.userservice_set.all():
            user_service: UserService
            if user_service.user_id != user.id:
                continue

            data.update(
                {
                    "linked": True,
                    "verified": user_service.last_verified.isoformat()
                    if user_service.last_verified
                    else False,
                    "scopes": user_service.scope.split(" "),
                    "identity": user_service.identity,
                }
            )

        await self.send(
            text_data=json.dumps(
                {
                    "class": "sb.users.services.status",
                    "service": service_name,
                    "data": data,
                }
            )
        )

    @database_sync_to_async
    def _twitch_refresh_user_token_cb(self, access_token, refresh_token):
        from service.models import Service, UserService

        user = self.scope["user"]
        twitch_service: Service = Service.object.get(name="twitch")
        user_service: UserService = UserService.object.get(
            service_id=twitch_service.id, user_id=user.id
        )

        user_service.user_token = access_token
        user_service.user_refresh_token = refresh_token
        user_service.save()

    async def _handle__vue_cb_verify_users_services(self, json_data={}):
        service_name = json_data["service"]
        user = self.scope["user"]
        user_service: UserService = await self.get_user_service(name=service_name)

        if not user_service:
            await self.send(
                text_data=json.dumps(
                    {
                        "class": "sb.verify.users.services",
                        "service": service_name,
                        "verify": False,
                        "scopes": [],
                        "message": "User Service not established, could not verify.",
                    }
                )
            )
            return

        if user_service.service.name == "twitch":
            from twitchapp.apps import TwitchAppConfig
            from twitchAPI.twitch import InvalidTokenException, MissingScopeException

            app: TwitchAppConfig = apps.get_app_config("twitchapp")
            tapi = await app.async_get_api(
                client_id=user_service.service.api_client_id,
                secret_key=user_service.service.api_secret_key,
            )
            tapi.user_auth_refresh_callback = self._twitch_refresh_user_token_cb

            try:
                await tapi.set_user_authentication(
                    token=user_service.user_token,
                    scope=[],
                    refresh_token=user_service.user_refresh_token,
                )
            except InvalidTokenException:
                await tapi.close()
                await self.send(
                    text_data=json.dumps(
                        {
                            "class": "sb.verify.users.services",
                            "service": service_name,
                            "verify": False,
                            "scopes": [],
                            "message": "Invalid token or incorrect token for user.",
                        }
                    )
                )
                return
            except MissingScopeException:
                await tapi.close()
                await self.send(
                    text_data=json.dumps(
                        {
                            "class": "sb.verify.users.services",
                            "service": service_name,
                            "verify": False,
                            "scopes": [],
                            "message": "Incorrect scope for provided token.",
                        }
                    )
                )
                return

            await tapi.close()

        last_verified = await self.update_user_service_verify_time(service_name)
        await self.send(
            text_data=json.dumps(
                {
                    "class": "sb.verify.users.services",
                    "service": service_name,
                    "scopes": user_service.scope,
                    "verify": last_verified,
                }
            )
        )

    async def _handle__vue_cb_users_services_oauth_flow(self, json_data={}):
        user = self.scope["user"]
        service_name = json_data["service"]
        code = json_data["code"]
        base_url = json_data["redirect_uri"]

        service = await self.get_service(name=service_name)
        request_params = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": service.api_client_id,
            "client_secret": service.api_secret_key,
            "redirect_uri": base_url,
            "scope": service.broad_scope,
        }

        print(request_params)

        # Request from OAuth Provider
        oauth_res = requests.post(
            url=service.oauth_endpoint_url,
            headers={"Content-Type": "application/json"},
            json=request_params,
        )
        upstream_json = oauth_res.json()

        print(upstream_json)

        if oauth_res.status_code in [400, 401]:
            await self.send(
                text_data=json.dumps(
                    {
                        "class": "sb.error",
                        "re_class": "vue.users.services.oauth.flow",
                        "message": "failed oauth request",
                    }
                )
            )
            return

        upstream_token = upstream_json["access_token"]
        self.twitch_access_token = upstream_token
        upstream_refresh = upstream_json.get("refresh_token")
        self.twitch_refresh_token = upstream_refresh
        upstream_scope = (
            upstream_json["scope"]
            if upstream_json.get("scope")
            else service.broad_scope
        )

        if service_name == "mastodon":
            # Todo: cross-reference mastodon ID
            pass
