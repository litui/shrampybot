from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from twitchapp.models import TwitchAccount
# from .serializers import StreamerSerializer


class StreamerSelfView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, format=None):
        user = User.objects.get(username=request.user.username)
        ta = user.streamer.twitchaccount

        u_obj = {
            "self": {
                "username": user.username,
                "isLoggedIn": True,
                "streamer": {
                    "identity": user.streamer.identity
                },
                "twitchAccount": {
                    "id": ta.twitch_id,
                    "login": ta.login,
                    "display_name": ta.display_name,
                    "description": ta.description,
                    "type": ta.account_type,
                    "broadcaster_type": ta.broadcaster_type
                }
            },
        }
        return Response(u_obj)

