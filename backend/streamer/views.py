from django.shortcuts import render
from .models import Streamer
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import StreamerSerializer

class StreamerCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer

class StreamerView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer

class StreamerUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer

class StreamerDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer
    
    # def get(self, request, pk=None):
    #     if pk:
    #         streamer = get_object_or_404(Streamer.objects.all(), pk=pk)
    #         return Response({
    #             "streamer", StreamerSerializer(streamer).data
    #         })

    #     streamers = StreamerSerializer(Streamer.objects.all(), many=True)
    #     return Response({"success": "true", "streamers": streamers.data})

    # def post(self, request):

    #     s = request.data.get('streamer')
    #     streamer = Streamer(
    #         twitch_login=s['twitch_login'],
    #         twitch_name=s['twitch_name'],
    #         twitch_id=s['twitch_id']
    #     )
    #     streamer.save()

    #     return Response({
    #         "success": "true",
    #         "message": "Streamer '{}' created successfully.".format(s['twitch_login'])
    #     })

    # def put(self, request, pk):
    #     s = request.data.get('streamer')
    #     streamer = Streamer.objects.filter(id=pk)
    #     streamer.update(
    #         twitch_login=s['twitch_login'],
    #         twitch_name=s['twitch_name'],
    #         twitch_id=s['twitch_id']
    #     )

    #     return Response({
    #         "success": "true",
    #         "message": "Streamer '{}' updated successfully.".format(s['twitch_login'])
    #     })

    # def delete(self, request, pk):
    #     streamer = get_object_or_404(Streamer.objects.all(), pk=pk)
    #     streamer.delete()

    #     return Response({
    #         "success": "true",
    #         "message": "Streamer with id `{}` has been deleted".format(pk)
    #     })
