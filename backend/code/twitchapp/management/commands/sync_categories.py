from django.apps.registry import apps
from ...apps import TwitchAppConfig
from django.core.management.base import BaseCommand, CommandError
from streamer.models import Streamer
from shrampybot.helpers import chunkify_list
from ...models import TwitchCategory
import json

class Command(BaseCommand):
    help = 'Updates (after initial setup) of Twitch categories via TwitchAPI.'

    def add_arguments(self, parser):
        parser.add_argument('field', nargs=1, type=str, choices=['twitch_id', 'name'])

    def handle(self, *args, **options):
        app: TwitchAppConfig = apps.get_app_config('twitchapp')
        api = app.api

        field = options['field'][0]

        results = []

        categories = TwitchCategory.objects.exclude(active=False)

        if field == 'twitch_id':
            params = [c.twitch_id for c in categories]
            for chunk in chunkify_list(params):
                results.extend(app.aiter(api.get_games(game_ids=chunk)))
            for category in categories:
                for result in results:
                    if category.twitch_id == result.id:
                        category.fill_from_twitch_category(result)
                        category.save()
        else:
            params = [c.name for c in categories]
            for chunk in chunkify_list(params):
                results.extend(app.aiter(api.get_games(names=chunk)))
            for category in categories:
                for result in results:
                    if category.name == result.name:
                        category.fill_from_twitch_category(result)
                        category.save()
        