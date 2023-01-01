from django.db import models
from streamer.models import Streamer
from service.models import Service
from twitchapp.models import TwitchStream
from uuid import uuid4


class Stream(models.Model):
    """Platform agnostic stream record"""

    guid = models.CharField(max_length=255, default=uuid4, unique=True, null=False)
    main_streamer = models.ForeignKey(Streamer, on_delete=models.RESTRICT)
    twitch_stream = models.OneToOneField(to=TwitchStream, on_delete=models.RESTRICT)
    hidden = models.BooleanField(default=False, null=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # def get_twitch_streams():
    #     from twitchapp.models import TwitchStream
    #     twitch_service = Service.objects.get(name='twitch')
    #     streams = Stream.objects.filter(platform=twitch_service)
    #     return streams

    def get_queryset():
        # Using '.all' to avoid caching.
        active = [i for i in Stream.objects.all() if i.twitch_stream.is_active]
        [i.refresh_from_db() for i in active]
        return active

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["main_streamer", "twitch_stream_id"], name="unique stream_assoc"
            )
        ]
