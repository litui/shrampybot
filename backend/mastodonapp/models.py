from django.db import models
from streamer.models import Streamer

# Create your models here.
class MastodonAccount(models.Model):
    from twitchapp.models import TwitchAccount

    mastodon_id = models.CharField(unique=True, max_length=255, null=False)
    acct = models.CharField(unique=True, max_length=255, null=False)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    primary_twitch_url = models.CharField(max_length=255, null=True)
    derived_twitch_id = models.CharField(max_length=255, null=True)
    twitch_account = models.ForeignKey(TwitchAccount, on_delete=models.RESTRICT, null=True)
    streamer = models.OneToOneField(Streamer, on_delete=models.RESTRICT)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)