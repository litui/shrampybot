from django_typomatic import ts_interface
from .models import Service, UserService
from rest_framework import serializers


@ts_interface()
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["name"]


@ts_interface()
class UserServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserService
        fields = ["identity", "service", "user", "scope", "last_verified"]

    service = ServiceSerializer(read_only=True, many=False)


@ts_interface()
class OAuthServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "name",
            "website_url",
            "broad_scope",
            "oauth_login_url",
            "oauth_endpoint_url",
            "oauth_revoke_url",
            "api_client_id",
        ]

    # name = serializers.CharField()
