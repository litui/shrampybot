import os
import logging
from logging import DEBUG, WARN, ERROR, INFO
from functools import cached_property
from twitchAPI import twitch
    

class TwitchHandler:
    def __init__(self):
        logger = logging.getLogger("TwitchHandler")
        self.l = logger.log
        self.l(INFO, "Initializing TwitchHandler")

    @cached_property
    def th(self):
        """Twitch Handler"""

        return twitch.Twitch(
            app_id=os.environ["TWITCH_API_KEY"],
            app_secret=os.environ["TWITCH_API_SECRET"]
        )

    def get_twitch_users(self, user_logins=[]):
        users = {
            i["login"]: i
            for i in self.th.get_users(
                logins=user_logins
            ).get("data", [])
        }

        return users