from django.shortcuts import render
from .models import Streamer
from rest_framework import generics, views
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import StreamerSerializer

class StreamerCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    
    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer

class StreamerSelfView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, format=None):
        u_obj = {
            "self": {
                "username": request.user.username,
                "isLoggedIn": True
            }
        }
        return Response(u_obj)

class StreamerView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer

class StreamerUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer

class StreamerDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer
