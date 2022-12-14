from django.apps.registry import apps
from django.shortcuts import render
from django.contrib.auth.models import User
from logging import log, INFO
from .models import Service, UserService
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework import generics, views
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import ServiceSerializer
import requests
from mastodon import Mastodon

class ServiceCreateView(generics.CreateAPIView):
    permission_classes = (IsAdminUser)
    
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceIndividualView(generics.RetrieveAPIView):
    lookup_field = 'name'
    lookup_url_kwarg = 'name'
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def post(self, request: Request, format=None, name=""):
        # log(INFO, request.query_params)
        if not request.query_params.get('action') in ['verify_user']:
            return Response(status=400, exception=True)

        code = request.data['code']
        referer = request.headers.get('Referer').split('?')[0]
        if not code or not name or not referer:
            return Response(status=400, exception=True)

        s_obj = Service.objects.get(name=name)
        request_params = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": s_obj.api_client_id,
            "client_secret": s_obj.api_secret_key,
            "redirect_uri": referer,
            "scope": s_obj.broad_scope
        }

        # Request from OAuth Provider
        oauth_res = requests.post(
            url=s_obj.oauth_endpoint_url,
            headers={'Content-Type': 'application/json'},
            json=request_params)
        upstream_json = oauth_res.json()
        
        if oauth_res.status_code in [400, 401]:
            return Response(status=oauth_res.status_code, exception=True)

        upstream_token = upstream_json['access_token']
        upstream_refresh = upstream_json.get('refresh_token')
        upstream_scope = upstream_json['scope'] if upstream_json.get('scope') else ''

        # Cross-reference twitch ID
        from twitchapp.apps import TwitchAppConfig
        from twitchapp.models import TwitchAccount

        app: TwitchAppConfig = apps.get_app_config('twitchapp')
        api = app.api

        app.arun(api.set_user_authentication(upstream_token, upstream_scope, upstream_refresh))
        t_user = app.aiter(api.get_users())[0]

        # check if twitch user is a guild member
        ta = TwitchAccount.objects.get(twitch_id=t_user.id, deleted=False)
        if not ta:
            return Response(status=403)

        # new_password = User.objects.make_random_password(
        #     length=32
        # )

        u_obj, user_created = User.objects.update_or_create(
            defaults={
                "is_active": True
            },
            username=ta.login
        )
        if user_created:
            u_obj.username = ta.login

        # Set and confirm temporary password (used for JWT, for now)
        # u_obj.set_password(new_password)
        u_obj.set_unusable_password()
        # if not u_obj.check_password(new_password):
        #     return Response(status=500, exception=True)

        # Save auth user
        u_obj.save()

        # Connect auth user with Twitch account 
        if ta.streamer and not ta.streamer.user:
            ta.streamer.user = u_obj
            ta.streamer.save()
        
        # Create user service to store third party credentials.
        us_obj, userservice_created = UserService.objects.get_or_create(
            defaults={
                "identity": ta.login,
                "service": s_obj,
                "user": u_obj,
                "scope": upstream_scope,
                "user_token": upstream_token,
                "user_refresh_token": upstream_refresh
            },
            service=s_obj,
            user=u_obj
        )
        us_obj.save()

        if not u_obj or not us_obj:
            return Response(status=500, exception=True)

        jwt_refresh = RefreshToken.for_user(u_obj)

        response = {
            "username": u_obj.username,
            "refresh": str(jwt_refresh),
            "access": str(jwt_refresh.access_token)
        }

        return Response(response)


class ServiceView(generics.ListAPIView):
    permission_classes = (IsAdminUser)

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser)

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser)

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
