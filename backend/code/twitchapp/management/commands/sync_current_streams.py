from django.apps.registry import apps
from django.db.models import ImageField
from ...apps import TwitchAppConfig
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from storages.base import Storage
from streamer.models import Streamer
from stream.models import Stream
from service.models import Service
from shrampybot.helpers import chunkify_list
from ...models import TwitchAccount, TwitchStream, TwitchCategory
from twitchAPI.twitch import Stream as TAPIStream
from uuid import uuid4
import requests


class Command(BaseCommand):
    help = "Update/add to the stream list with the current streaming list."

    def handle(self, *args, **options):
        app: TwitchAppConfig = apps.get_app_config("twitchapp")
        api = app.api

        ids = [a.twitch_id for a in TwitchAccount.objects.exclude(twitch_id=None)]

        user_objects: list[TAPIStream] = []

        for chunk in chunkify_list(ids):
            user_objects.extend(app.aiter(api.get_streams(first=100, user_id=chunk)))

        active_twitch_ids = [u.id for u in user_objects]

        for stream in user_objects:
            try:
                category = TwitchCategory.objects.get(twitch_id=stream.game_id)
            except TwitchCategory.DoesNotExist:
                continue

            account = TwitchAccount.objects.get(twitch_id=stream.user_id)

            thumbnail_parsed = stream.thumbnail_url.replace(
                "{width}x{height}", "1280x720"
            )
            response = requests.get(thumbnail_parsed)
            thumbnail_file = ContentFile(
                content=response.content, name=str(uuid4()) + ".jpg"
            )

            twitch_stream, created = TwitchStream.objects.update_or_create(
                defaults={
                    "twitch_id": stream.id,
                    "twitch_account": account,
                    "twitch_category": category,
                    "type": stream.type,
                    "title": stream.title,
                    "viewer_count": stream.viewer_count,
                    "started_at": stream.started_at,
                    "language": stream.language,
                    "thumbnail_url": stream.thumbnail_url,
                    "thumbnail_image": thumbnail_file,
                    "is_mature": stream.is_mature,
                    "is_active": True,
                },
                twitch_id=stream.id,
            )
            twitch_stream.save()
            # twitch_stream.thumbnail_image.name = uuid4
            # twitch_stream.thumbnail_image.write(response.text)
            # twitch_stream.thumbnail_image.save(name=str(uuid4()), content=response.text)

        existing_active_streams = TwitchStream.objects.filter(is_active=True)
        for stream in existing_active_streams:
            if not stream.twitch_id in active_twitch_ids:
                stream.is_active = False
                stream.save()

        print("Populated/updated: {} stream(s)".format(len(user_objects)))
