from .models import Streamer, StreamerAct
from rest_framework import serializers
from django.contrib.auth.models import User
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


class SelfStreamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'is_authenticated',
            'is_superuser',
            'is_staff',
            'isLoggedIn',
            'streamer'
        ]

    streamer = StreamerSerializer(many=False, read_only=True)
    isLoggedIn = serializers.BooleanField(read_only=True, default=True)

class StreamerActSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamerAct
        fields = [
            'guid',
            'visual_name',
            'twitch_url',
            'irl_location',
            'e_mail',
            'now',
            'next',
            'later',
            'notes',
            'alt_email',
            'twitch_account'
        ]
    
    twitch_account = TwitchAccountSerializer(many=False, read_only=True)