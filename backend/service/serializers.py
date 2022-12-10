from .models import Service
from rest_framework import serializers

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ["api_token", "api_secret_key", "api_refresh_token"]
    id = serializers.IntegerField()
    name = serializers.CharField()
    website_url = serializers.CharField()
    broad_scope = serializers.CharField()
    oauth_endpoint_url = serializers.CharField()