from django_typomatic import ts_interface
from .models import Stream
from django.db.models import OuterRef
from twitchapp.models import TwitchAccount, TwitchStream
from streamer.serializers import StreamerSerializer
from service.serializers import ServiceSerializer
from twitchapp.serializers import TwitchStreamSerializer
from rest_framework import serializers


@ts_interface()
class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ["guid", "main_streamer", "twitch_stream"]

    main_streamer = StreamerSerializer(read_only=True, many=False)
    # platform = ServiceSerializer(read_only=True, many=False)
    twitch_stream = TwitchStreamSerializer(instance=TwitchStream)
    # platform_stream = TwitchStreamSerializer()


# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

#     class Meta:
#         model = Album
#         fields = ['album_name', 'artist', 'tracks']
# id = serializers.IntegerField()
# twitch_login = serializers.CharField()
# twitch_name = serializers.CharField()
# twitch_id = serializers.CharField()
# created_date = serializers.DateTimeField()
# modified_date = serializers.DateTimeField()
