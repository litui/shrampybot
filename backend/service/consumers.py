import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from streamer.serializers import SelfStreamerSerializer

GROUP_NAME_GENERAL_NOTIFICATIONS = 'notif_general'
GROUP_NAME_STAFF_NOTIFICATIONS = 'notif_staff'
GROUP_NAME_TWITCH_EVENTSUB = 'twitch_eventsub'


class ServiceConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self._msg_class_map = {
            'vue.logout': self._handle__vue_logout,
            'vue.cb.render.sidebar': self._handle__vue_cb_render_sidebar,
            'vue.cb.route.push': self._handle__vue_cb_route_push,
        }
        self._allowed_groups = []
        super().__init__(*args, **kwargs)

    @database_sync_to_async
    def get_self_user(self):
        return SelfStreamerSerializer(self.scope['user']).data

    async def connect(self):
        if self.scope['user'].is_authenticated:
            await self.accept()
            serialized_output = await self.get_self_user()

            self._allowed_groups.append(GROUP_NAME_GENERAL_NOTIFICATIONS)
            if self.scope['user'].is_staff:
                self._allowed_groups.append(GROUP_NAME_STAFF_NOTIFICATIONS)

            for group_name in self._allowed_groups:
                # Auto subscribe to the right groups for the user level
                await self.channel_layer.group_add(group_name, self.channel_name)

            await self.send(text_data=json.dumps({
                "class": "sb.users.self",
                "data": serialized_output,
            }))
        else:
            await self.disconnect(403)

    async def disconnect(self, close_code):
        for group_name in self.groups:
            await self.channel_layer.group_discard(group_name, self.channel_name)
        self._allowed_groups = []
        await self.close(close_code)

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        msg_class = json_data.get('class', 'unknown')

        try:
            await self._msg_class_map[msg_class](json_data)

        except (IndexError, KeyError):
            await self.send(text_data=json.dumps({
                "class": "sb.error",
                "message": "Failed to interpret sent message type."
            }))

    async def _handle__vue_logout(self, json_data={}):
        await self.send(text_data=json.dumps({
            "class": "sb.logout",
            "message": "Disconnecting by user request."
        }))
        self.disconnect(200)


    async def _handle__vue_cb_route_push(self, json_data={}):
        pass
        # await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def _handle__vue_cb_render_sidebar(self, json_data={}):
        pass