from django.apps.registry import apps
from .apps import TwitchAppConfig
from rest_framework.views import APIView

class TwitchEventView (APIView):
    app: TwitchAppConfig = apps.get_app_config('twitchapp')
    api = app.api

    