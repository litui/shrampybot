from django.apps.registry import apps
from ...apps import TwitchAppConfig
from django.core.management.base import BaseCommand, CommandError
from streamer.models import Streamer
from shrampybot.helpers import chunkify_list
from ...models import TwitchAccount, TwitchStream, TwitchCategory

class Command(BaseCommand):
    help = 'Update/add to the stream list with the current streaming list.'

    def handle(self, *args, **options):
        app: TwitchAppConfig = apps.get_app_config('twitchapp')
        api = app.api

        ids = [a.twitch_id for a in TwitchAccount.objects.exclude(twitch_id=None)]
            
        user_objects = []

        for chunk in chunkify_list(ids):
            user_objects.extend(app.aiter(api.get_streams(first=100, user_id=chunk)))

        active_twitch_ids = [u.id for u in user_objects]

        for stream in user_objects:
            try:
                category = TwitchCategory.objects.get(twitch_id=stream.game_id)
            except TwitchCategory.DoesNotExist:
                continue

            twitch_stream, created = TwitchStream.objects.update_or_create(
                defaults={
                    'twitch_id': stream.id,
                    'twitch_account': TwitchAccount.objects.get(twitch_id=stream.user_id),
                    'twitch_category': category,
                    'type': stream.type,
                    'title': stream.title,
                    'viewer_count': stream.viewer_count,
                    'started_at': stream.started_at,
                    'language': stream.language,
                    'thumbnail_url': stream.thumbnail_url,
                    'is_mature': stream.is_mature,
                    'is_active': True
                },
                twitch_id=stream.id
            )
            twitch_stream.save()

        existing_active_streams = TwitchStream.objects.filter(is_active=True)
        for stream in existing_active_streams:
            if not stream.twitch_id in active_twitch_ids:
                stream.is_active = False
                stream.save()

        print("Populated/updated: {} stream(s)".format(len(user_objects)))