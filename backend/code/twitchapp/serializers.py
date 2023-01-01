from django_typomatic import ts_interface
from .models import TwitchAccount, TwitchStream
from rest_framework import serializers


@ts_interface()
class TwitchAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitchAccount
        fields = ["login", "display_name", "twitch_id", "description"]

    # id = serializers.IntegerField()
    # twitch_login = serializers.CharField()
    # twitch_name = serializers.CharField()
    # twitch_id = serializers.CharField()
    # created_date = serializers.DateTimeField()
    # modified_date = serializers.DateTimeField()


@ts_interface()
class TwitchStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitchStream
        fields = [
            "twitch_id",
            "twitch_category",
            "title",
            "started_at",
            "language",
            "is_mature",
            "thumbnail_url",
            "thumbnail_image",
            "is_active",
        ]
