from django.apps import AppConfig


class StreamerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "streamer"

    def ready(self):
        from .models import StreamerAct
        from django.dispatch import receiver
        # from gsheets.signals import sheet_row_processed
        from django.core.exceptions import ObjectDoesNotExist

        # @receiver(sheet_row_processed, sender=StreamerAct)
        # def populate_twitch_logins(
        #     instance: StreamerAct = None, created=None, row_data=None, **kwargs
        # ):
        #     from twitchapp.models import TwitchAccount

        #     try:
        #         instance.refresh_from_db()
        #         if instance.twitch_login:
        #             (
        #                 instance.twitch_account,
        #                 created,
        #             ) = TwitchAccount.objects.update_or_create(
        #                 defaults={"display_name": instance.twitch_login},
        #                 login=instance.twitch_login,
        #             )
        #         instance.save()

        #     except (ObjectDoesNotExist, KeyError):
        #         pass
