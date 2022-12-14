import asyncio
import threading
from functools import cached_property
from django.apps import AppConfig
from twitchAPI import twitch


class TwitchAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'twitchapp'
    verbose_name = "Twitch App"

    def ready(self):
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

        return self.arun(self._get_api(
            twitch_service.api_client_id,
            twitch_service.api_secret_key
        ))

    async def _get_api(self, client_id, secret_key):
        await asyncio.sleep(0.5)
        t = await twitch.Twitch(
            app_id=client_id,
            app_secret=secret_key
        )
        return t

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
