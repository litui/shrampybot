from django.db import models
from streamer.models import Streamer

class DiscordAccount(models.Model):
    discord_id = models.CharField(unique=True, max_length=255, null=False)
    discord_name_in_guild = models.CharField(max_length=255, unique=True, null=False)
    parsed_twitch_url = models.CharField(max_length=255, unique=False)
    streamer = models.OneToOneField(Streamer, on_delete=models.RESTRICT, null=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)