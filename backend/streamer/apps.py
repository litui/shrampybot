from django.apps import AppConfig


class StreamerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'streamer'

    def ready(self):
        from .models import StreamerAct
        from django.dispatch import receiver
        from gsheets.signals import sheet_row_processed
        from django.core.exceptions import ObjectDoesNotExist

