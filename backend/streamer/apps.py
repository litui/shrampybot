from django.apps import AppConfig


class StreamerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'streamer'

    def ready(self):
        from .models import StreamerAct
        from django.dispatch import receiver
        from gsheets.signals import sheet_row_processed
        from django.core.exceptions import ObjectDoesNotExist

        @receiver(sheet_row_processed, sender=StreamerAct)
        def populate_twitch_logins(instance: StreamerAct=None, created=None, row_data=None, **kwargs):
            from twitchapp.models import TwitchAccount
            try:
                if instance.twitch_login:
                    instance.twitch_account, created = TwitchAccount.objects.get_or_create(
                        login=instance.twitch_login
                    )
                    # instance.twitch_account.populate_fields_from_twitch()
                    instance.twitch_account.save()
                    instance.save()

            except (ObjectDoesNotExist, KeyError):
                pass
