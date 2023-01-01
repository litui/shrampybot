from .models import Streamer, StreamerAct
from django_typomatic import ts_interface
from rest_framework import serializers
from django.contrib.auth.models import User
from twitchapp.serializers import TwitchAccountSerializer


@ts_interface()
class StreamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streamer
        fields = [
            "identity",
            "guild_status",
            "shrampybot_announce",
            "retired",
            "retired_date",
            "twitchaccount",
        ]

    twitchaccount = TwitchAccountSerializer(many=False, read_only=True)
    # id = serializers.IntegerField()
    # twitch_login = serializers.CharField()
    # twitch_name = serializers.CharField()
    # twitch_id = serializers.CharField()
    # created_date = serializers.DateTimeField()
    # modified_date = serializers.DateTimeField()


@ts_interface()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "is_authenticated",
            "is_superuser",
            "is_staff",
            "password",
            "streamer",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    streamer = StreamerSerializer(many=False, read_only=True)

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


@ts_interface()
class StreamerActSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamerAct
        fields = [
            "guid",
            "visual_name",
            "twitch_url",
            "irl_location",
            "e_mail",
            "now",
            "next",
            "later",
            "notes",
            "alt_email",
            "twitch_account",
        ]

    twitch_account = TwitchAccountSerializer(many=False, read_only=True)
