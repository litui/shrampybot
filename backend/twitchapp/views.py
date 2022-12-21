from django.apps.registry import apps
from .apps import TwitchAppConfig
from rest_framework.views import APIView

class TwitchEventSubView (APIView):
    app: TwitchAppConfig = apps.get_app_config('twitchapp')
    _api = app.api

    