import os
import logging
from logging import DEBUG, WARN, ERROR, INFO
from functools import cached_property
import hikari
from hikari import HikariError as DiscordError


class DiscordHandler:

    def __init__(self):
        logger = logging.getLogger("DiscordHandler")
        self.l = logger.log
        self.l(INFO, "Initializing DiscordHandler")

    @cached_property
    def _dh(self):
        retval = None
        rest = hikari.RESTApp()
        retval = rest.acquire(
            token=os.environ['DISCORD_TOKEN'],
            token_type=hikari.applications.TokenType.BOT
        )
        retval.start()
        return retval

    @cached_property
    async def _me(self):
        return await self._dh.fetch_my_user()

    async def send_message(self, msg, image=None):
        image_attach = None
        if image:
            image_attach = hikari.Bytes(
                image,
                "image.jpg",
                mimetype="image/jpeg"
            )
        message = await self._dh.create_message(
            channel=os.environ["DISCORD_CHANNEL"],
            content=msg,
            attachment=image_attach,
            flags=hikari.MessageFlag.SUPPRESS_EMBEDS
        )
        try:
            await self._dh.crosspost_message(
                channel=os.environ["DISCORD_CHANNEL"],
                message=message
            )
        except hikari.HikariError as e:
            self.l(WARN, "Could not crosspost message {}".format(
                message.id
            ))
        
        return message