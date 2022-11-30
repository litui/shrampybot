import logging
import hmac, binascii, hashlib
from functools import cached_property
from logging import DEBUG, INFO, ERROR, WARN
from auth.generic import GenericAuthenticator
from lib.s3 import S3
from lib.twitch import TwitchHandler


HMAC_PREFIX = "sha256="


class TwitchAuthenticator(GenericAuthenticator):
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger("TwitchAuthenticator")
        self.l = logger.log
        self.l(INFO, "Initializing TwitchAuthenticator")

        self.verify = self.entry_point
        super().__init__(*args, **kwargs)

        self._s3 = S3()
        self._th = TwitchHandler()

        self._secret = self._env["TWITCH_EVENT_SECRET"].encode("utf-8")
        self._message_id = \
            self._headers.get(self._th.TWITCH_MESSAGE_ID)
        self._signature = \
            self._headers.get(self._th.TWITCH_MESSAGE_SIGNATURE)
        self._timestamp = \
            self._headers.get(self._th.TWITCH_MESSAGE_TIMESTAMP)

    @cached_property
    def _calculated_signature(self) -> str:
        h = hmac.HMAC(key=self._secret, digestmod="sha256")
        h.update(
            self._message_id.encode("utf-8") +
            self._timestamp.encode("utf-8") +
            self._body_raw.encode("utf-8")
        )
        hex_digest = binascii.hexlify(h.digest()).decode("utf-8")
        return HMAC_PREFIX + hex_digest

    async def check_credentials(self):
        self.l(INFO, "Verifying request origin.")
        if not self._secret \
                or not self._message_id \
                or not self._timestamp \
                or not self._signature \
                or not self._calculated_signature:
            self.l(DEBUG, "Could not verify Twitch credentials.")
            return False
    
        if self._calculated_signature == self._signature:
            return True

        return False

    async def check_for_replay(self):
        self.l(INFO, "Mitigating replay attacks.")
        return self._s3.check_and_stow_event_message_id(
            self._message_id, self._body
        )