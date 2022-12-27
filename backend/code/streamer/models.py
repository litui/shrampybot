from django.db import models
from django.contrib.auth.models import User
from gsheets import mixins
from uuid import uuid4
from shrampybot.helpers import get_twitch_id_from_url


class Streamer(models.Model):
    class GuildStatusType(models.TextChoices):
        FRY = "fry", "Shrimp Fry (Pre-event)"
        SHRIMP = "shrimp", "Shrimp (1+ events)"
        SHRAMP = "shramp", "Shramp (4+ events)"
        SCAMPI = "scampi", "Scampi Shramp (OG)"

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.RESTRICT, null=True)
    identity = models.CharField(max_length=255, unique=True)
    guild_status = models.CharField(
        max_length=30, choices=GuildStatusType.choices, default=GuildStatusType.FRY
    )
    shrampybot_announce = models.BooleanField(default=True, null=False)
    retired = models.BooleanField(default=False, null=False)
    retired_date = models.DateTimeField(null=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)


class StreamerAct(mixins.SheetSyncableMixin, models.Model):
    from twitchapp.models import TwitchAccount

    model_id_field = "guid"
    sheet_name = "MasterStreamerList"

    # streamer = models.ForeignKey(Streamer, on_delete=models.RESTRICT, null=True)
    guid = models.CharField(primary_key=True, max_length=255, default=uuid4)

    visual_name = models.CharField(max_length=255, null=False)
    twitch_url = models.CharField(max_length=255, null=True)
    irl_location = models.CharField(max_length=255, null=True)
    e_mail = models.CharField(max_length=255, null=True)
    now = models.CharField(max_length=255, null=True)
    next = models.CharField(max_length=255, null=True)
    later = models.CharField(max_length=255, null=True)
    notes = models.TextField(null=True)
    alt_email = models.CharField(max_length=255, null=True)
    twitch_account = models.ForeignKey(
        TwitchAccount, on_delete=models.RESTRICT, null=True
    )
    # streamer = models.ForeignKey(Streamer, on_delete=models.RESTRICT, null=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def twitch_login(self):
        return get_twitch_id_from_url(self.twitch_url)
