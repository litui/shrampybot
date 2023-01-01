from django.apps import AppConfig


class StreamerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "streamer"

    def ready(self):
        from .models import StreamerAct
        from twitchapp.models import TwitchAccount
        from django.core.exceptions import ObjectDoesNotExist
        from django.dispatch import receiver
        from django.db.models.signals import post_save

        @receiver(post_save, sender=StreamerAct)
        def link_streamer_and_login(**kwargs):
            sa: StreamerAct = kwargs["instance"]

            if sa.twitch_login:
                account, created = TwitchAccount.objects.update_or_create(
                    login=sa.twitch_login
                )

                # Verify account exists before saving association on create
                if created:
                    # TODO: Add Twitch query code
                    pass
                sa.twitch_account = account
                sa.save()
