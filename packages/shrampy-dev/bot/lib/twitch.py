import os
import logging
from logging import DEBUG, WARN, ERROR, INFO
from functools import cached_property
from twitchAPI import twitch, eventsub, types
from lib.helper import chunkify


class TwitchHandler:
    TWITCH_MESSAGE_ID = 'twitch-eventsub-message-id'
    TWITCH_MESSAGE_TIMESTAMP = 'twitch-eventsub-message-timestamp'
    TWITCH_MESSAGE_SIGNATURE = 'twitch-eventsub-message-signature'
    TWITCH_MESSAGE_TYPE = 'twitch-eventsub-message-type'

    def __init__(self):
        logger = logging.getLogger("TwitchHandler")
        self.l = logger.log
        self.l(INFO, "Initializing TwitchHandler")
        self._team_name = os.environ["TWITCH_TEAM_NAME"]

    @cached_property
    def _th(self):
        """Twitch Handler"""

        return twitch.Twitch(
            app_id=os.environ["TWITCH_API_KEY"],
            app_secret=os.environ["TWITCH_API_SECRET"]
        )

    @cached_property
    def _eh(self):
        """Event Handler"""

        eh = eventsub.EventSub(
            callback_url=os.environ["EVENTSUB_URL"],
            api_client_id=os.environ["TWITCH_API_KEY"],
            port=443,
            twitch=self._th
        )
        eh.secret = os.environ["TWITCH_EVENT_SECRET"]
        eh.unsubscribe_on_stop = False
        eh.wait_for_subscription_confirm = False
        return eh

    @cached_property
    def event_subs(self):
        return self._th.get_eventsub_subscriptions().get("data", [])

    @cached_property
    def team_info(self):
        self.l(DEBUG, "Accessed team_info cached property.")
        team = {}
        if self._team_name:
            team = self._th.get_teams(name=self._team_name).get("data", [])
            if team:
                return team.pop()

        return team

    @property
    def _event_streamon_users(self):
        return [
            i["condition"]["broadcaster_user_id"]
            for i in self.event_subs
            if i["type"] == "stream.online"
        ]

    @property
    def _event_streamoff_users(self):
        return [
            i["condition"]["broadcaster_user_id"]
            for i in self.event_subs
            if i["type"] == "stream.offline"
        ]

    @property
    def _event_raid_users(self):
        return [
            i["condition"]["from_broadcaster_user_id"]
            for i in self.event_subs
            if i["type"] == "channel.raid"
        ]

    def get_users(self, user_logins=[]):
        # Limit to 100 per request
        users = {}
        for user_chunk in chunkify(user_logins):
            users.update({
                i["login"]: i
                for i in self._th.get_users(
                    logins=user_chunk
                ).get("data", [])
            })
        return users

    def get_stream_by_user_id(self, user_id):
        streams = self._th.get_streams(first=1, user_id=user_id).get("data", [])
        return streams.pop() if streams else {}

    def _null_cb(self, data):
        '''NULL callback for use with listen_ eventsub calls.'''
        pass

    def subscribe_to_events(self, twitch_users):
        new_streamon_count = 0
        new_streamoff_count = 0
        new_raid_count = 0

        for u, data in twitch_users.items():
            uid = data["id"]
            if not uid in self._event_streamon_users:
                try:
                    self._eh.listen_stream_online(
                        broadcaster_user_id=uid,
                        callback=self._null_cb
                    )
                    new_streamon_count += 1
                except types.EventSubSubscriptionConflict as e:
                    self.l(DEBUG, "Event conflict on uid '{}', event '{}'"
                        .format(uid, "stream.online")
                    )

            if not uid in self._event_streamoff_users:
                try:
                    self._eh.listen_stream_offline(
                        broadcaster_user_id=uid,
                        callback=self._null_cb
                    )
                    new_streamoff_count += 1
                except types.EventSubSubscriptionConflict as e:
                    self.l(DEBUG, "Event conflict on uid '{}', event '{}'"
                        .format(uid, "stream.offline")
                    )

            if not uid in self._event_raid_users:
                try:
                    self._eh.listen_channel_raid(
                        from_broadcaster_user_id=uid,
                        callback=self._null_cb
                    )
                    new_raid_count += 1
                except types.EventSubSubscriptionConflict as e:
                    self.l(DEBUG, "Event conflict on uid '{}', event '{}'"
                        .format(uid, "channel.raid")
                    )
                
        newbies = new_streamon_count + \
            new_streamoff_count + \
            new_raid_count
        if newbies:
            try:
                del self.event_subs
            except AttributeError:
                pass

        return self.event_subs

    def unsubscribe_all_events(self):
        self._eh.unsubscribe_all()
        return True
