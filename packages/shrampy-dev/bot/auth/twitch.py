import logging
from logging import DEBUG, INFO, ERROR, WARN
from auth.generic import GenericAuthenticator

TWITCH_MESSAGE_ID = 'twitch-eventsub-message-id'
TWITCH_MESSAGE_TIMESTAMP = 'twitch-eventsub-message-timestamp'
TWITCH_MESSAGE_SIGNATURE = 'twitch-eventsub-message-signature'
TWITCH_MESSAGE_TYPE = 'twitch-eventsub-message-type'


class TwitchAuthenticator(GenericAuthenticator):
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger("TwitchAuthenticator")
        self.l = logger.log
        self.l(INFO, "Initializing TwitchAuthenticator")

        self.verify = self.entry_point
        super().__init__(*args, **kwargs)

    async def check_credentials(self):
        return False