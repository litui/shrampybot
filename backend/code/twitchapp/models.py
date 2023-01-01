from django.apps.registry import apps
from django.db import models
from django.dispatch import receiver
from streamer.models import Streamer
from uuid import uuid4
from .apps import TwitchAppConfig
from twitchAPI.twitch import TwitchUser as _TwitchUser, Game as _Game, Stream as _Stream
from asgiref.sync import async_to_sync, sync_to_async


class TwitchAccount(models.Model):
    class TwitchAccountType(models.TextChoices):
        USER = "", "User"
        STAFF = "staff", "Staff"
        GLOBAL_MOD = "global_mod", "Global Mod"
        ADMIN = "admin", "Admin"

    class TwitchBroadcasterType(models.TextChoices):
        BASIC = "", "Basic"
        AFFILIATE = "affiliate", "Affiliate"
        PARTNER = "partner", "Partner"

    login = models.CharField(max_length=255, unique=True, null=False)
    display_name = models.CharField(max_length=255, unique=True, null=True)
    twitch_id = models.CharField(max_length=255, unique=True, null=True)
    description = models.TextField(null=True)
    profile_image_url = models.TextField(null=True)
    offline_image_url = models.TextField(null=True)
    email = models.EmailField(null=True)
    account_type = models.CharField(
        max_length=20, choices=TwitchAccountType.choices, default=TwitchAccountType.USER
    )
    broadcaster_type = models.CharField(
        max_length=20,
        choices=TwitchBroadcasterType.choices,
        default=TwitchBroadcasterType.BASIC,
    )
    deleted = models.BooleanField(null=False, default=False)
    twitch_created_at = models.DateTimeField(null=True)
    streamer = models.OneToOneField(Streamer, on_delete=models.RESTRICT, null=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def fill_from_twitch_user(self, user: _TwitchUser):
        self.twitch_id = user.id
        self.login = user.login
        self.display_name = user.display_name
        self.description = user.description
        self.account_type = user.type
        self.broadcaster_type = user.broadcaster_type
        self.twitch_created_at = user.created_at
        self.profile_image_url = user.profile_image_url
        self.offline_image_url = user.offline_image_url

    def update_twitch_account_by_login(self):
        app: TwitchAppConfig = apps.get_app_config("twitchapp")
        api = app.api

        if self.login:
            users = async_to_sync(api.get_users(logins=[self.login]))
            print(users)


class TwitchCategory(models.Model):
    twitch_id = models.CharField(max_length=40, unique=True, null=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    box_art_url = models.CharField(max_length=255, null=True)
    active = models.BooleanField(null=False, default=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def fill_from_twitch_category(self, category: _Game):
        self.twitch_id = category.id
        self.name = category.name
        self.box_art_url = category.box_art_url


class TwitchStream(models.Model):
    twitch_id = models.CharField(max_length=40, unique=True)
    twitch_account = models.ForeignKey(TwitchAccount, on_delete=models.RESTRICT)
    twitch_category = models.ForeignKey(TwitchCategory, on_delete=models.RESTRICT)
    type = models.CharField(max_length=20, default="live", null=False)
    title = models.TextField(null=True)
    viewer_count = models.IntegerField(null=False, default=0)
    started_at = models.DateTimeField(null=False, db_index=True)
    language = models.CharField(max_length=20, null=True)
    thumbnail_url = models.CharField(max_length=255, null=True)
    thumbnail_image = models.ImageField(null=True, upload_to="uploads/%Y/%m/%d/")
    is_mature = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=False, default=True, db_index=True)
    ended_at = models.DateTimeField(null=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def fill_from_twitch_stream(self, stream: _Stream):
        self.twitch_id = stream.id
        self.twitch_account = TwitchAccount.objects.get(twitch_id=stream.user_id)
        self.twitch_category = TwitchCategory.objects.get(twitch_id=stream.game_id)
        self.type = stream.type
        self.title = stream.title
        self.viewer_count = stream.viewer_count
        self.started_at = stream.started_at
        self.language = stream.language
        self.thumbnail_url = stream.thumbnail_url
        self.is_mature = stream.is_mature

    def get_active_twitch_ids():
        return [i.twitch_id for i in TwitchStream.objects.filter(is_active=True)]

    def get_related_stream(self):
        from service.models import Service
        from stream.models import Stream

        service = Service.objects.get(name="twitch")

        return Stream.objects.get(platform=service, platform_stream_id=self.twitch_id)
