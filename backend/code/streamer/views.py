from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import StreamerAct
from .serializers import UserSerializer, StreamerActSerializer

# from .serializers import StreamerSerializer


class StreamerSelfView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"self": serializer.data})


class StreamerActsListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    lookup_field = "guid"
    lookup_url_kwarg = "guid"
    queryset = StreamerAct.objects.all().order_by("visual_name")
    serializer_class = StreamerActSerializer
