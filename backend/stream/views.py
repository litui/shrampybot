from django.shortcuts import render
from rest_framework import generics
from .models import Stream
from .serializers import StreamSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class StreamView(generics.ListAPIView):
    lookup_field = 'guid'
    lookup_url_kwarg = 'guid'
    queryset = Stream.get_active_streams()
    serializer_class = StreamSerializer
    
    permission_classes = (IsAuthenticated,)