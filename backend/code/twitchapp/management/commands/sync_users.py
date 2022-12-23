from django.apps.registry import apps
from ...apps import TwitchAppConfig
from django.core.management.base import BaseCommand, CommandError
from streamer.models import Streamer
from shrampybot.helpers import chunkify_list
from ...models import TwitchAccount

class Command(BaseCommand):
    help = 'Populates/updates existing entries in the Twitch account list'

    def add_arguments(self, parser):
        parser.add_argument('field', nargs=1, type=str, choices=['login', 'twitch_id'])
        parser.add_argument('value', nargs='?', type=str)

    def handle(self, *args, **options):
        app: TwitchAppConfig = apps.get_app_config('twitchapp')
        api = app.api

        field = options['field'][0]
        value = options.get('value')

        if options.get('value'):
            if field == 'login':
                print("Match by login: {}".format(value))
                accounts = [TwitchAccount.objects.get(login=value)]
            else:
                print("Match by id: {}".format(value))
                accounts = [TwitchAccount.objects.get(twitch_id=value)]
        else:
            if field == 'login':
                print("Match by login (all)")
                accounts = TwitchAccount.objects.exclude(login=None)
            else:
                print("Match by id (all)")
                accounts = TwitchAccount.objects.exclude(twitch_id=None)
            
        user_objects = []

        if field == 'login':
            all_params = [a.login for a in accounts]
            for logins in chunkify_list(all_params):
                user_objects.extend(app.aiter(api.get_users(logins=logins)))
            for account in accounts:
                for user in user_objects:
                    if account.login == user.login:
                        account.fill_from_twitch_user(user)
                        account.save()

        else:
            all_params = [a.twitch_id for a in accounts]
            for ids in chunkify_list(all_params):
                user_objects.extend(app.aiter(api.get_users(user_ids=ids)))
            for account in accounts:
                for user in user_objects:
                    if account.twitch_id == user.id:
                        account.fill_from_twitch_user(user)
                        account.save()

        # Attaching and updating Streamers
        # for account in accounts:
        #     if not account.streamer:
        #         account.streamer = Streamer(identity=account.display_name)
        #         account.streamer.save()
        #         account.save()

        print("Accounts: {}".format(len(accounts)))
        print("User Objects: {}".format(len(user_objects)))

