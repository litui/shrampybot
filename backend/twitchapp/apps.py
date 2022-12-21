import asyncio
import threading
from channels.db import database_sync_to_async
from functools import cached_property
from django.apps import AppConfig
from twitchAPI import twitch, eventsub


class TwitchAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'twitchapp'
    verbose_name = "Twitch App"

    def ready(self):

        from django.dispatch import receiver
        from django.db.models.signals import post_save
        from .models import TwitchStream
        from service.models import Service
        from stream.models import Stream
        from streamer.models import Streamer

        @receiver(post_save, sender=TwitchStream)
        def create_generic_stream(**kwargs):
            ts: TwitchStream = kwargs['instance']

            stream, created = Stream.objects.update_or_create(
                main_streamer=ts.twitch_account.streamer,
                twitch_stream=ts
            )

        from .models import TwitchAccount

        @receiver(post_save, sender=TwitchAccount)
        def create_generic_streamer(**kwargs):
            ta: TwitchAccount = kwargs['instance']

            ta.streamer, created = Streamer.objects.update_or_create(
                defaults={
                    "identity": ta.display_name if ta.display_name else ta.login
                },
                identity=ta.display_name
            )

        # Handling of async api
        # brilliant approach via:
        # https://stackoverflow.com/questions/70231451/wrapping-python-async-for-synchronous-execution

        def spawn_thread(loop: asyncio.AbstractEventLoop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self._async_loop = asyncio.new_event_loop()
        thread = threading.Thread(
            target=spawn_thread,
            args=(self._async_loop,),
            daemon=True
        )
        thread.start()

    @cached_property
    def api(self) -> twitch.Twitch:
        from service.models import Service

        twitch_service = Service.objects.get(name='twitch')

        return self.arun(self.async_get_api(
            twitch_service.api_client_id,
            twitch_service.api_secret_key
        ))

    @database_sync_to_async
    def _refresh_app_token_cb(self, access_token):
        from service.models import Service

        twitch_service: Service = Service.object.get(name="twitch")
        twitch_service.api_token = access_token
        twitch_service.save()

    async def async_get_api(self, client_id, secret_key):
        t = await twitch.Twitch(
            app_id=client_id,
            app_secret=secret_key
        )
        t.app_auth_refresh_callback = self._refresh_app_token_cb
        return t

    @cached_property
    def eventsub(self) -> eventsub.EventSub:
        from service.models import Service

        twitch_service = Service.objects.get(name='twitch')
        # Touch this cached property to make sure it happens
        # before the self.arun is called.
        self.api

        eh = self.arun(self.async_get_eventsub(
            twitch_service.webhooks_inbound_endpoint,
            twitch_service.api_client_id,
            self.api
        ))
        eh.secret = twitch_service.webhooks_shared_secret
        eh.unsubscribe_on_stop = False
        eh.wait_for_subscription_confirm = False
        return eh

    async def async_get_eventsub(self, cb_url, client_id, twitch_api):
        eh = await eventsub.EventSub(
            callback_url=cb_url,
            api_client_id=client_id,
            port=443,
            twitch=twitch_api
        )
        eh.secret = twitch_api.webhooks_shared_secret
        eh.unsubscribe_on_stop = False
        eh.wait_for_subscription_confirm = False
        return eh

    def arun(self, coroutine):
        """Runner of async coroutines returning results in sync"""
        thread = asyncio.run_coroutine_threadsafe(coroutine, self._async_loop).result()
        return thread

    def aiter(self, agen):
        """Shorthand for arun(aiter(...))"""
        return self.arun(self._aiter(agen))

    async def _aiter(self, agen):
        """Iterator for async generators"""
        await asyncio.sleep(0.5)
        collection = []
        async for i in agen:
            collection.append(i)
        return collection
