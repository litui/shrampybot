from .models import Streamer
from rest_framework import serializers

class StreamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streamer
        fields = '__all__'
    # id = serializers.IntegerField()
    # twitch_login = serializers.CharField()
    # twitch_name = serializers.CharField()
    # twitch_id = serializers.CharField()
    # created_date = serializers.DateTimeField()
    # modified_date = serializers.DateTimeField()