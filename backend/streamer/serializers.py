from .models import Streamer
from rest_framework import serializers
from twitchapp.serializers import TwitchAccountSerializer

class StreamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streamer
        fields = [
            'identity', 
            'guild_status', 
            'shrampybot_announce', 
            'retired',
            'retired_date',
            'twitchaccount'
        ]

    twitchaccount = TwitchAccountSerializer(
        many=False,
        read_only=True
    )
    # id = serializers.IntegerField()
    # twitch_login = serializers.CharField()
    # twitch_name = serializers.CharField()
    # twitch_id = serializers.CharField()
    # created_date = serializers.DateTimeField()
    # modified_date = serializers.DateTimeField()