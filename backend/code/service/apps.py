from django.apps import AppConfig
from django_typomatic import generate_ts


class ServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "service"

    def ready(self):
        from django.dispatch import receiver
        from django.db.backends.signals import connection_created

        @receiver(connection_created)
        def database_connected(connection, **kwargs):
            """Generate TypeScript file once at app launch.

            This generates for the entire suite of models, not
            just within this app.
            """
            print("Outputting TypeScript definitions for the frontend")
            generate_ts("../model-ts/all.ts")