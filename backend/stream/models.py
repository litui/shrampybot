from django.db import models
from streamer.models import Streamer
from service.models import Service
from twitchapp.models import TwitchStream
from uuid import uuid4


class Stream(models.Model):
    """Platform agnostic stream record"""

    guid = models.CharField(max_length=255, default=uuid4, null=False, unique=False)
    main_streamer = models.ForeignKey(Streamer, on_delete=models.RESTRICT)
    platform = models.ForeignKey(Service, on_delete=models.RESTRICT)
    platform_stream_id = models.CharField(max_length=255, null=False)
    hidden = models.BooleanField(default=False, null=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def platform_stream(self):
        if self.platform.name == 'twitch':
            return TwitchStream.objects.get(twitch_id=self.platform_stream_id)

    def get_active_streams():
        active = [i.stream for i in TwitchStream.objects.filter(is_active=True)]
        [i.refresh_from_db() for i in active]
        return active

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['main_streamer', 'platform', 'platform_stream_id'], name='unique stream_assoc')
        ]
