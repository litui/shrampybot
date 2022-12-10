from django.db import models

class Streamer(models.Model):
    on_mastodon = models.BooleanField(null=False, default=False)
    mastodon_id = models.TextField(unique=True, null=True)
    on_twitch = models.BooleanField(null=False, default=False)
    twitch_login = models.TextField(unique=True, null=True)
    twitch_name = models.TextField(unique=True, null=True)
    twitch_id = models.TextField(unique=True, null=True)
    in_twitch_team = models.BooleanField(null=False, default=False)
    on_discord = models.BooleanField(null=False, default=False)
    discord_id = models.TextField(unique=True, null=True)
    twitch_uri_in_mastodon_fields = models.BooleanField(null=False, default=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
