import os
import re
from functools import cached_property
import urllib.request
from mastodon import Mastodon
from twitchAPI.twitch import Twitch
from twitchAPI.eventsub import EventSub
import hikari
from hikari import Intents
import asyncio
import hmac, binascii, hashlib
import json

# Notification request headers
TWITCH_MESSAGE_ID = 'Twitch-Eventsub-Message-Id'.lower()
TWITCH_MESSAGE_TIMESTAMP = 'Twitch-Eventsub-Message-Timestamp'.lower()
TWITCH_MESSAGE_SIGNATURE = 'Twitch-Eventsub-Message-Signature'.lower()
TWITCH_MESSAGE_TYPE = 'Twitch-Eventsub-Message-Type'.lower()

# Prepend this string to the HMAC that's created from the message
HMAC_PREFIX = 'sha256=';


class SocialHandler:
    def __init__(self):
        self.event_map = {
            "stream.online": self.stream_online_cb,
            "stream.offline": self.stream_offline_cb,
            "channel.raid": self.raidout_cb
        }

    ### Properties

    @cached_property
    def dh(self):
        if self.use_discord:
            rest = hikari.RESTApp()
            return rest.acquire(
                token=os.environ['DISCORD_TOKEN'],
                token_type=hikari.applications.TokenType.BOT
            )
            
        return None

    @cached_property
    def th(self):
        """Twitch Handler"""

        return Twitch(
            app_id=os.environ["TWITCH_API_KEY"],
            app_secret=os.environ["TWITCH_API_SECRET"]
        )

    @cached_property
    def eh(self):
        """Event Handler"""

        return EventSub(
            callback_url=os.environ["EVENTSUB_URL"],
            api_client_id=os.environ["TWITCH_API_KEY"],
            port=443,
            twitch=self.th
        )

    @cached_property
    def mh(self):
        """Mastodon Handler"""

        return Mastodon(
            access_token=os.environ["MASTODON_API_TOKEN"],
            api_base_url=os.environ["MASTODON_API_URL"]
        )

    @cached_property
    def me(self):
        return self.mh.me()

    @cached_property
    def accounts_full(self):
        return {i.get("acct"): i.get("fields") 
            for i in [j.get("account") for j in self.mh.admin_accounts()]
            if i.get("bot") == False}

    @cached_property
    def twitch_users(self):
        users = self.th.get_users(logins=[t.get("twitch_id", "") for m,t in self.m_to_t_map.items()]).get("data", [])
        return users

    @cached_property
    def m_to_t_map(self):
        mapped_accounts = self.account_map.copy()

        for account,data in self.accounts_full.items():
            for field in data:
                data_map = {}

                # Check if field contains Twitch URL
                res = re.findall(
                    pattern=r"\"(?:https?:\/\/)?(?:www\.)?twitch\.tv\/([A-Za-z0-9_-]+)\/?\"",
                    string=field["value"],
                    flags=re.I
                )
                if len(res) == 1:
                    data_map["twitch_id"] = res[0].lower()
                else:
                    res = re.findall(
                        pattern=r"(?:https?:\/\/)?(?:www\.)?twitch\.tv\/([A-Za-z0-9_-]+)\/?",
                        string=field["value"],
                        flags=re.I
                    )
                    if len(res) == 1:
                        data_map["twitch_id"] = res[0].lower()

                if data_map:
                    mapped_accounts[account] = data_map
                    break

        return mapped_accounts

    @cached_property
    def twitch_event_subs(self):
        return self.th.get_eventsub_subscriptions()

    ### Callbacks

    def stream_online_cb(self, data):
        print(json.dumps(data))
        # Don't go further if stream type is incorrect
        type = data.get("type")
        if type != "live":
            return {
                "body": {
                    "error": "Stream type is not 'live'."
                }
            }

        # Fail if no active streams on query
        user_id = data.get("broadcaster_user_id")
        streams = self.th.get_streams(user_id=user_id).get("data", []);
        if not streams:
            return {
                "body": {
                    "user": user_id,
                    "data": data,
                    "error": "Querying for streams produced no results."
                }
            }
        stream = streams[0]

        # Fail if incorrect category
        category = stream.get("game_name", "")
        if category not in self.categories.keys():
            return {
                "body": {
                    "error": "Category {} not in acceptable categories list."
                             .format(category)
                }
            }

        # Check for existing toots
        stream_id_h = self.get_twitch_id_hash(
            stream.get("id"), prefix="tw"
        )
        if self.get_toot_by_twitch_id(stream_id_h):
            return {
                "body": {
                    "error": "Stream ID {} already posted."
                    .format(stream_id_h)
                }
            }

        # Fail if login doesn't concern us
        user_login = stream.get("user_login", "")
        user_name = stream.get("user_name", "")
        focus_logins = {t.get("twitch_id", "").lower(): m for m,t in self.m_to_t_map.items()}
        if not user_name.lower() in focus_logins.keys():
            return {
                "body": {
                    "error": "{} not a user login mapped in Mastodon."
                             .format(user_login)
                }
            }

        # Start actually making a new post
        media_ids = []
        mature = stream.get("is_mature", False)
        thumb_url = stream.get("thumbnail_url", "")
        sized_url = re.sub(
            "\{width\}x\{height\}",
            "{}x{}".format(1280, 720),
            thumb_url)
        thumb = None
        if thumb_url:
            thumb = self.fetch_twitch_thumbnail(sized_url)
            thumb_desc = "Preview of {}'s stream on Twitch.".\
                         format(user_name)
            media_ids.append(
                self.mh.media_post(thumb, "image/jpeg", thumb_desc)
            )
        stream_url = "https://twitch.tv/{}".format(user_name)
        stream_title = stream.get("title", "")
        broadcaster = focus_logins.get(user_login.lower())
        message = "@{} is now doing {} on Twitch: {}\n\n{}\n\n#gsg {}\n#{}" \
                  .format(
                    broadcaster,
                    category,
                    stream_url,
                    stream_title,
                    self.categories[category],
                    stream_id_h
                  )
        toot = self.mh.status_post(
            status=message,
            visibility=os.environ["MASTODON_POST_MODE"],
            media_ids=media_ids,
            sensitive=mature,
            spoiler_text="@{}'s {} stream info (marked as \"mature\" on Twitch)".format(broadcaster, category) if mature else None
        )
        if self.use_discord:
            discord_message = "*Via Mastodon ({}):*\n{} is now doing {} on Twitch: {}\n\n{}\n\n[{}]" \
                .format(
                    toot["url"],
                    user_name,
                    category,
                    stream_url,
                    stream_title,
                    stream_id_h
                )
            self.discord_send_message(discord_message, stream_id_h, thumb)
        return {
            "body": toot.get("id")
        }

    def stream_offline_cb(self, data):
        print(json.dumps(data))
        return {"body": data}

    def raidout_cb(self, data):
        print(json.dumps(data))
        return {"body": data}

    ### Functions

    def discord_send_message(self, msg, nonce, attach=None):
        loop = asyncio.get_event_loop_policy().get_event_loop()
        return loop.run_until_complete(self._discord_send_message(msg, nonce, attach))

    async def _discord_send_message(self, msg, nonce, attach=None):
        if attach:
            image = hikari.Bytes(attach, "image.jpg", mimetype="image/jpeg")
        else:
            image = None
        async with self.dh as client:
            message = await client.create_message(
                channel=os.environ["DISCORD_CHANNEL"],
                content=msg,
                attachment=image,
                flags=hikari.MessageFlag.SUPPRESS_EMBEDS
                    | hikari.MessageFlag.CROSSPOSTED)
            return message

    def get_twitch_id_hash(self, id, prefix="TW"):
        # print("Input ID: {}".format(id))
        h = hashlib.md5(id.encode("utf-8"), usedforsecurity=False)
        dig = prefix + h.hexdigest()[0:8]
        # print("Output ID: {}".format(dig))
        return dig

    def fetch_twitch_thumbnail(self, url):
        thumb = b""
        with urllib.request.urlopen(url) as f:
            thumb = f.read()
        return thumb

    def get_toot_by_twitch_id(self, twitch_id):
        return self.mh.account_statuses(
            id=self.me.get("id"),
            tagged=twitch_id)

    def process_notification(self):
        subscription = self.body.get("subscription", {})
        event = self.body.get("event", {})

        callback = self.event_map.get(subscription.get("type"))

        if callback:
            return callback(event)

    def subscribe_events(self):
        subs = self.twitch_event_subs
        print(json.dumps(subs))
        self.eh.secret = os.environ["TWITCH_EVENT_SECRET"]
        self.eh.unsubscribe_on_stop = False
        self.eh.wait_for_subscription_confirm = False

        subdata = subs.get("data", [])
        streamon_users = [i["condition"]["broadcaster_user_id"] for i in subdata if i["type"] == "stream.online"]
        streamoff_users = [i["condition"]["broadcaster_user_id"] for i in subdata if i["type"] == "stream.offline"]
        raidout_users = [i["condition"]["from_broadcaster_user_id"] for i in subdata if i["type"] == "channel.raid"]

        new_streamon_count = 0
        new_streamoff_count = 0
        new_raidout_count = 0

        for u in self.twitch_users:
            if u["id"] not in streamon_users:
                self.eh.listen_stream_online(
                    broadcaster_user_id=u["id"],
                    callback=self.stream_online_cb
                )
                new_streamon_count += 1

            # if u["id"] not in streamoff_users:
            #     self.eh.listen_stream_offline(
            #         broadcaster_user_id=u["id"],
            #         callback=self.stream_offline_cb
            #     )
            #     new_streamoff_count += 1

            # if u["id"] not in raidout_users:
            #     self.eh.listen_channel_raid(
            #         from_broadcaster_user_id=u["id"],
            #         callback=self.raid_out_cb
            #     )
            #     new_raidout_count += 1

        newbies = new_streamon_count + \
            new_streamoff_count + \
            new_raidout_count
        if newbies:
            del(self.__dict__["twitch_event_subs"])

        subs = self.twitch_event_subs
        return {"body": subs}

    def unsubscribe_all_events(self):
        self.eh.unsubscribe_all()
        return {"body": {"unsubscribed": "all"}}

    def verify_origin(self):
        result = False

        try:
            secret = os.environ["TWITCH_EVENT_SECRET"].encode("utf-8")
            message_id = self.headers.get(TWITCH_MESSAGE_ID, "")
            timestamp = self.headers.get(TWITCH_MESSAGE_TIMESTAMP, "")
            h = hmac.HMAC(key=secret, digestmod="sha256")
            h.update(
                message_id.encode("utf-8") + 
                timestamp.encode("utf-8") + 
                self.body_raw.encode("utf-8"))
            my_sig = HMAC_PREFIX + binascii.hexlify(h.digest()).decode("utf-8")
            print("Locally Generated Signature: {}".format(my_sig))
            print("Twitch Generated Signature : {}".format(self.headers.get(TWITCH_MESSAGE_SIGNATURE, "")))
            result = my_sig == self.headers.get(TWITCH_MESSAGE_SIGNATURE, "")
        except Exception as e:
            print(e)

        return result

    def route_request(self, args):
        self.headers = args.get("__ow_headers", {})
        self.method = args.get("__ow_method", {})
        self.path = args.get("__ow_path", {})
        self.body_raw = args.get("__ow_body", "")
        self.use_discord = args.get("post_to_discord", False)
        self.account_map = args.get("cross_instance_account_map", {})
        self.categories = args.get("twitch_category_hashtag_map", {})
        self.body = json.loads(self.body_raw)

        override = self.body.get("override", "");
        override_token = self.body.get("override_token", "");
        if override and override_token:
            if override_token == os.environ["OVERRIDE_TOKEN"]:
                if override == "subscribe":
                    return self.subscribe_events()
                if override == "unsubscribe":
                    return self.unsubscribe_all_events()
                if override == "discord_send":
                    dismsg = self.body.get("discord_message", "")
                    if dismsg:
                        self.discord_send_message(dismsg)
                        return {"body": {"msg": "success"}}

        msg_type = self.headers.get(TWITCH_MESSAGE_TYPE)

        if msg_type == "webhook_callback_verification":
            return {
                "headers": {
                    "content-type": "text/plain"
                },
                "body": self.body.get("challenge", "")
            }
        
        if msg_type == "notification":
            if not self.verify_origin():
                return {"body": {"error": "origin verification failed"}}
            else:
                return self.process_notification()
        if msg_type == "revoke":
            return {
                "body": {"msg": "Accepted revocation."}
            }

        return {"body": self.body}
        # return {"body": dict(os.environ)}


def main(args):
    """Main process routine"""
    # return {"body": args}

    s = SocialHandler()
    return s.route_request(args)
