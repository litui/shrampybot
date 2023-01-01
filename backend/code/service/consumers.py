import json
from typing import Tuple
from django.apps.registry import apps
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from streamer.serializers import UserSerializer
from .serializers import UserServiceSerializer
from .models import Service, UserService
from datetime import datetime
import requests
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import (
    GenericAsyncAPIConsumer,
    AsyncAPIConsumer,
)
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)

GROUP_NAME_GENERAL_NOTIFICATIONS = "notif_general"
GROUP_NAME_STAFF_NOTIFICATIONS = "notif_staff"
GROUP_NAME_TWITCH_EVENTSUB = "twitch_eventsub"


class ServiceConsumer(AsyncAPIConsumer):
    """A monolithic async consumer for the web UI"""

    def __init__(self, *args, **kwargs):
        # self._msg_class_map = {
        #     "vue.logout": self._handle__vue_logout,
        #     "vue.cb.render.sidebar": self._handle__vue_cb_render_sidebar,
        #     "vue.cb.route.push": self._handle__vue_cb_route_push,
        #     "vue.get.users.services.status": self._handle__vue_cb_users_services_status,
        #     "vue.verify.users.services": self._handle__vue_cb_verify_users_services,
        #     "vue.users.services.oauth.flow": self._handle__vue_cb_users_services_oauth_flow,
        # }
        # self._allowed_groups = []
        super().__init__(*args, **kwargs)

    @action()
    def retrieve_self(self, **kwargs) -> Tuple[ReturnDict, int]:
        """Retrieval of the logged-in user.

        :return: User serializer data and code 200
        :rtype: Tuple[ReturnDict, int]
        """
        instance = self.scope["user"]
        serializer = UserSerializer(instance=instance)
        return serializer.data, status.HTTP_200_OK
