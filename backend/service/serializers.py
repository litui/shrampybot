from .models import Service
from rest_framework import serializers

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name']

    name = serializers.CharField()

class OAuthServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'name',
            'website_url',
            'broad_scope',
            'oauth_login_url',
            'oauth_endpoint_url',
            'oauth_revoke_url',
            'api_client_id'
        ]

    # name = serializers.CharField()