from django.db import models
from streamer.models import Streamer
from service.models import Service


class StreamingPlatform(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    api_info = models.OneToOneField(Service, on_delete=models.RESTRICT)


class Stream(models.Model):
    """Platform agnostic stream record"""

    streamer = models.ManyToManyField(Streamer)
    hidden = models.BooleanField(default=False, null=False)
    

class StreamAssoc(models.Model):
    """Associates abstract streams with their platform-based feeds."""

    platform = models.ForeignKey(StreamingPlatform, on_delete=models.RESTRICT)
    stream = models.ForeignKey(Stream, on_delete=models.RESTRICT)
    platform_stream_id = models.CharField(max_length=255, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['platform', 'stream', 'platform_stream_id'], name='unique stream_assoc')
        ]
