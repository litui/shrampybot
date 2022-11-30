import re
import os
import logging
from logging import DEBUG, INFO, ERROR, WARN
from functools import cached_property
from mastodon import Mastodon, MastodonError

class MastodonHandler:
    def __init__(self):
        logger = logging.getLogger("MastodonHandler")
        self.l = logger.log
        self.l(INFO, "Initializing MastodonHandler object.")

    @cached_property
    def _mh(self):
        self.l(DEBUG, "Connecting to Mastodon.")
        return Mastodon(
            access_token=os.environ["MASTODON_API_TOKEN"],
            api_base_url=os.environ["MASTODON_API_URL"]
        )

    @cached_property
    def _accounts(self):
        self.l(DEBUG, "Fetching and cacheing accounts.")
        accts = [
            i for i in [
                j.account for j in self._mh.admin_accounts()
            ]
            if i.bot == False]
        return accts

    @cached_property
    def twitch_map(self):
        self.l(DEBUG, "Compiling mastodon to twitch ID mapping.")
        map = {}
        map_reverse = {}
        for account in self._accounts:
            for field in account.fields:
                twitch_id = self._extract_twitch_id_from_url(field.value)
                if twitch_id:
                    if not map.get(account.acct):
                        map[account.acct] = []
                    if not twitch_id in map[account.acct]:
                        map[account.acct].append(twitch_id)

        for mastodon_id, twitch_ids in map.items():
            for twitch_id in twitch_ids:
                if not map_reverse.get(twitch_id):
                    map_reverse[twitch_id] = []
                if not mastodon_id in map_reverse[twitch_id]:
                    map_reverse[twitch_id].append(mastodon_id)
        return {
            "m_to_t": map,
            "t_to_m": map_reverse
        }

    @cached_property
    def _me(self):
        self.l(DEBUG, "Fetching information about Mastodon API user.")
        return self._mh.me()

    def _extract_twitch_id_from_url(self, field_value):
        # Within quotes
        res = re.findall(
            pattern=r"\"(?:https?:\/\/)?(?:www\.)?twitch\.tv\/([A-Za-z0-9_-]+)\/?\"",
            string=field_value,
            flags=re.I
        )
        if len(res) == 1:
            return res[0].lower()
        else:
            # Without quotes.
            res = re.findall(
                pattern=r"(?:https?:\/\/)?(?:www\.)?twitch\.tv\/([A-Za-z0-9_-]+)\/?",
                string=field_value,
                flags=re.I
            )
            if len(res) == 1:
                return res[0].lower()

        return None

    def upload_jpeg(self, image, description):
        return self._mh.media_post(
            media_file=image,
            mime_type="image/jpeg",
            description=description
        )