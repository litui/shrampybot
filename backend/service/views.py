from django.shortcuts import render
from django.contrib.auth.models import User
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
        upstream_scope = upstream_json['scope']

        # Part two: get Mastodon user info if we're talking about Mastodon
        m = Mastodon(
            access_token=upstream_token,
            api_base_url=s_obj.website_url
        )
        me = m.me()
        new_password = User.objects.make_random_password(
            length=32
        )

        u_obj, user_created = User.objects.update_or_create(
            defaults={
                "is_active": True
            },
            username=me.username
        )
        u_obj.set_password(new_password)
        if not u_obj.check_password(new_password):
            return Response(status=500, exception=True)
        u_obj.save()

        us_obj, userservice_created = UserService.objects.get_or_create(
            defaults={
                "identity": me.acct,
                "service": s_obj,
                "user": u_obj,
                "scope": upstream_scope,
                "user_token": upstream_token,
                "user_refresh_token": "none"
            },
            service=s_obj,
            user=u_obj
        )
        us_obj.save()

        if not u_obj or not us_obj:
            return Response(status=500, exception=True)

        return Response({
            "username": u_obj.username,
            "temp_password": new_password,
            "created_user": user_created,
            "created_userservice": userservice_created
        })


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

class UserServiceValidator(views.APIView):
    def post(self, request: Request, format=None, name=""):
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
        upstream_scope = upstream_json['scope']

        # Part two: get Mastodon user info if we're talking about Mastodon
        m = Mastodon(
            access_token=upstream_token,
            api_base_url=s_obj.website_url
        )
        me = m.me()
        new_password = User.objects.make_random_password(
            length=32
        )

        u_obj, user_created = User.objects.update_or_create(
            defaults={
                "is_active": True
            },
            username=me.username
        )
        u_obj.set_password(new_password)
        if not u_obj.check_password(new_password):
            return Response(status=500, exception=True)
        u_obj.save()

        us_obj, userservice_created = UserService.objects.get_or_create(
            defaults={
                "identity": me.acct,
                "service": s_obj,
                "user": u_obj,
                "scope": upstream_scope,
                "user_token": upstream_token,
                "user_refresh_token": "none"
            },
            service=s_obj,
            user=u_obj
        )
        us_obj.save()

        if not u_obj or not us_obj:
            return Response(status=500, exception=True)

        return Response({
            "username": u_obj.username,
            "temp_password": new_password,
            "created_user": user_created,
            "created_userservice": userservice_created
        })
