import asyncio
import logging
from logging import DEBUG, WARN, ERROR, INFO
from auth.admin import AdminAuthenticator
from auth.twitch import TwitchAuthenticator
from lib.s3 import S3, CachedDataRetrievalError
from lib.mastodon import MastodonHandler
from lib.twitch import TwitchHandler
from lib.helper import twitch_date, fetch_twitch_thumb
from controllers.generic import GenericController
from datetime import timedelta, datetime
import time

class EventController(GenericController):
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger("EventController")
        self.l = logger.log
        self.l(INFO, "Initializing EventController.")
        self._admin_auth = AdminAuthenticator(*args, **kwargs)
        self._twitch_auth = TwitchAuthenticator(*args, **kwargs)
        super().__init__(*args, **kwargs)

        self._mh = MastodonHandler()
        self._th = TwitchHandler()
        self._s3 = S3()

        self._message_type = self._headers.get(
            self._th.TWITCH_MESSAGE_TYPE
        )

        self._event_map = {
            "stream.online": self._stream_online_cb,
            "stream.offline": self._stream_offline_cb,
            "channel.raid": self._channel_raid_cb
        }

    async def entry_point(self):
        if len(self._path) > 1 and self._path[1] == "twitch":
            # if await self._twitch_auth.check_for_replay():
            #     return {
            #         "body": self._router.call_error(17),
            #         "statusCode": 409
            #     }
            if not await self._twitch_auth.check_credentials():
                return {
                    "body": self._router.call_error(14),
                    "statusCode": 403
                }
        else:
            if not await self._admin_auth.check_credentials():
                return {
                    "body": self._router.call_error(14),
                    "statusCode": 403
                }

        return await super().entry_point()

    async def _patch__event_sub(self):
        """Subscribe to events."""
        self.l(INFO, "Subscribing to events.")
        users = self._s3.twitch_users
        return {
            "body": self._th.subscribe_to_events(users),
            "statusCode": 200
        }

    async def _delete__event_sub(self):
        """Unsubscribe from events."""
        self._th.unsubscribe_all_events()
        return {
            "body": "",
            "statusCode": 204
        }

    async def _get__event_category(self):
        return {
            "body": self._s3.category_map,
            "statusCode": 200
        }
        pass

    async def _post__event_category(self):
        categories = self._body.get("categories", {})

        for category, tags in categories.items():
            self._s3.add_category(category, tags)
        return {
            "body": self._s3.category_map,
            "statusCode": 200
        }

    async def _delete__event_category(self):
        pass

    async def _post__event_twitch(self):
        """Handler for Twitch events."""
        status_code = 204
        body_out = ""
        headers_out = {
            "Content-Type": "text/plain"
        }

        if self._message_type == "webhook_callback_verification":
            status_code = 200
            body_out = self._body.get("challenge")

        elif self._message_type == "revocation":
            self.l(WARN, "Received revocation: {}".format(
                self._body.get("subscription")
            ))

        elif self._message_type == "notification":
            sub = self._body.get("subscription", {})
            sub_type = sub.get("type", "")

            self.l(INFO, "Received {} notification.".format(
                sub_type
            ))

            # Callbacks for webhook handling
            event_func = self._event_map.get(sub_type)
            await event_func(
                self._body.get("event", {})
            )

        return {
            "body": body_out,
            "headers": headers_out,
            "statusCode": status_code
        }

    async def _new_mastodon_msg(self, user, stream, meta={}, thumb=b""):
        self.l(INFO, "Preparing toot.")
        display_name = user["display_name"]
        login_name = user["login"]
        stream_url = "https://twitch.tv/{}".format(login_name)
        stream_title = stream.get("title", "")
        mastodon_ids = self._s3.tm_map.get("login_name", [])
        category = stream["game_name"]
        tags = self._s3.category_map[category].get("mastodon_tags")
        mature = stream.get("is_mature", False)

        media_ids = []
        if thumb:
            thumb_desc = "Preview of {}'s stream on Twitch"\
                .format(display_name)
            media_ids.append(
                self._mh.upload_jpeg(
                    image=thumb,
                    description=thumb_desc
                )
            )
            meta["mastodon_media_ids"] = media_ids
        
        # Link to mastodon user if there is one, otherwise
        # just post the Twitch Names
        verb = "are" if len(mastodon_ids) > 1 else "is"
        if mastodon_ids:
            streamers = ", ".join(["@{}".format(i) for i in mastodon_ids])
        else:
            streamers = display_name

        await asyncio.sleep(0.5)

        # Formulate (English for now) message
        message = "{} {} now streaming {} on Twitch: {}\n\n{}\n\n{}" \
            .format(
                streamers,
                verb,
                category,
                stream_url,
                stream_title,
                tags
            )

        toot = self._mh._mh.status_post(
            status=message,
            visibility=self._env["MASTODON_POST_MODE"],
            media_ids=media_ids,
            sensitive=mature,
            spoiler_text=None,
            idempotency_key=stream["id"]
        )
        meta["last_toot"] = toot.id
        # Meta must be saved outside this function.

        self.l(INFO, "Toot sent: {}".format(toot.id))
        
        await asyncio.sleep(0.5)
        return toot.id

    async def _new_discord_msg(self, user, stream, meta, thumb_url=""):
        await asyncio.sleep(0.5)
        return -1

    # TWITCH EVENTSUB CALLBACKS

    async def _stream_online_cb(self, event):
        self.l(INFO, "Checking event type.")
        # Don't go further if stream type is incorrect
        type = event.get("type")
        if type != "live":
            return {
                "body": {
                    "error": "Stream type is not 'live'."
                }
            }

        self.l(INFO, "Retrieving cached user record.")
        received_time = time.time()
        # Get cached user record
        # Should be up to date as of the last PATCH of
        # /user/twitch
        user_id = event["broadcaster_user_id"]
        users = [
            data for u, data in self._s3.twitch_users.items()
            if data["id"] == user_id
        ]
        if not users:
            raise CachedDataRetrievalError()
        user = users.pop()
        user_login = user["login"]
        
        self.l(INFO, "Checking if debounce is needed.")
        # Check last stream disconnect time (in seconds)
        interval = int(
            self._env.get("STREAMUP_DEBOUNCE_INTERVAL", "600")
        )
        meta = self._s3.stream_meta.get(user_id, {})
        if meta:
            last_ended = meta.get("last_stream_ended", 0)
            delta = received_time - last_ended
            if delta <= interval:
                self.l(WARN, "Debouncing new stream posting due to "
                    "too short an offline time.")
                return

        self.l(INFO, "Retrieving live stream information.")
        # Get and cache stream information
        stream = self._th.get_stream_by_user_id(user_id)
        self._s3.update_stream_cache(user_id, stream)
        self.l(INFO, "Stream ID: {}".format(stream["id"]))
        
        self.l(INFO, "Checking stream category.")
        # Check if stream category is one we care about
        category = stream.get("game_name")
        if category not in self._s3.category_map.keys():
            self.l(INFO, "New '{}' stream is not in a supported category."
                .format(category)
            )
            return

        # Record stream ID
        meta["last_stream_id"] = stream["id"]

        self.l(INFO, "Preparing thumbnail.")
        thumb = fetch_twitch_thumb(stream["thumbnail_url"])
        thumb_url = self._s3.stow_thumb_as_file(stream["id"], thumb)
        
        loop = asyncio.get_event_loop_policy().get_event_loop()
        toot_id, discord_id = await asyncio.gather(
            self._new_mastodon_msg(user, stream, meta, thumb),
            self._new_discord_msg(user, stream, meta, thumb_url),
            loop=loop
        )

        # Mandatory updating of stream meta.
        self._s3.update_stream_meta(user_id, meta)

    async def _stream_offline_cb(self, event):
        user_id = event["broadcaster_user_id"]
        self.l(INFO, "Logging stream offline time for {}".format(
            user_id
        ))
        
        self.l(INFO, "Retrieving and adjusting cached user record.")
        received_time = time.time()
        meta = self._s3.stream_meta.get(user_id, {})
        meta["last_stream_ended"] = received_time
        self._s3.update_stream_meta(user_id, meta)

    async def _channel_raid_cb(self, event):
        pass
