from django.core.management.base import BaseCommand, CommandError
from service.models import Service
from twitchapp.models import TwitchCategory
import json

class Command(BaseCommand):
    help = 'Initial (first time) setup of API services from json.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs=1, type=str)

    def handle(self, *args, **options):
        with open(options['json_file'][0], 'r') as initfile:
            json_init = json.load(initfile)

        for heading, section in json_init.items():
            if heading == 'services':
                cr_count = 0
                up_count = 0
                for name, service in section.items():
                    result, created = Service.objects.update_or_create(
                        defaults={
                            "website_url": service['rest_url'],
                            "broad_scope": service['user_scope'],
                            "oauth_login_url": service['oauth_auth_url'],
                            "oauth_endpoint_url": service['oauth_token_url'],
                            "oauth_revoke_url": service['oauth_revoke_url'],
                            "api_client_id": service['api_client_id'],
                            "api_secret_key": service['api_secret_key'],
                            "api_token": service['api_token'],
                            "api_refresh_token": service['api_refresh_token']
                        },
                        name=name
                    )
                    if created:
                        cr_count += 1
                    else:
                        up_count += 1
                print("Created {} services".format(cr_count))
                print("Updated {} services".format(up_count))

            if heading == 'twitch':
                for subheading, subsection in section.items():
                    if subheading == 'categories':
                        cr_count = 0
                        up_count = 0
                        for name in subsection.keys():
                            result, created = TwitchCategory.objects.update_or_create(
                                name=name
                            )
                            if created:
                                cr_count += 1
                            else:
                                up_count += 1
                        print("Created {} Twitch categories".format(cr_count))
                        print("Updated {} Twitch categories".format(up_count))
