import os
import json
import logging
from logging import DEBUG, INFO, WARN, ERROR
from functools import cached_property
from lib import bucketstore
from botocore.errorfactory import ClientError


class S3:
    def __init__(self):
        logger = logging.getLogger("S3")
        self.l = logger.log
        self.l(logging.INFO, "Initializing S3 object.")
        self._bucket_name = os.environ['AWS_BUCKET']
        self._custom_pair_path = "custom_pairs"
        self._m_to_t_path = "mastodon_to_twitch"
        self._t_to_m_path = "twitch_to_mastodon"
        self._twitch_user_path = "twitch_users"

    @cached_property
    def _bucket(self):
        self.l(DEBUG, "Accessing root bucket.")
        return bucketstore.get(
            bucket_name=self._bucket_name,
            create=True
        )

    @cached_property
    def mt_map(self):
        self.l(DEBUG, "Accessed mt_map cached property.")
        try:
            map = json.loads(self._bucket[self._m_to_t_path])
        except ClientError:
            self.l(WARN, "Accessed mastodon_map key before creation.")
            return {}
        self.l(DEBUG, "mt_map property: {}".format(map))
        return map
        
    @cached_property
    def tm_map(self):
        self.l(DEBUG, "Accessed tm_map cached property.")
        try:
            map = json.loads(self._bucket[self._t_to_m_path])
        except ClientError:
            self.l(WARN, "Accessed twitch_map key before creation.")
            return {}
        self.l(DEBUG, "tm_map property: {}".format(map))
        return map

    @cached_property
    def twitch_users(self):
        self.l(DEBUG, "Accessed twitch_users cached property.")
        try:
            users = json.loads(self._bucket[self._twitch_user_path])
        except ClientError:
            self.l(WARN, "Accessed twitch_users key before creation.")
            return {}
        self.l(DEBUG, "twitch_users property: {}".format(users))
        return users

    @cached_property
    def custom_pairs(self):
        self.l(DEBUG, "Accessed custom pairs cached property.")
        try:
            pairs = json.loads(self._bucket[self._custom_pair_path])
        except ClientError:
            self.l(WARN, "Accessed custom pairs key before creation.")
            return {}
        return pairs

    @cached_property
    def custom_mt_map(self):
        self.l(DEBUG, "Accessed custom_mt_map cached property.")
        map = {}
        pairs = self.custom_pairs
        for pair in pairs:
            m_id = pair.get("mastodon_id")
            t_id = pair.get("twitch_login")
            if not m_id or not t_id:
                continue
            if not m_id in map.keys():
                map[m_id] = []
            if not t_id in map[m_id]:
                map[m_id].append(t_id)
        return map

    @cached_property
    def custom_tm_map(self):
        self.l(DEBUG, "Accessed custom_tm_map cached property.")
        map = {}
        pairs = self.custom_pairs
        for pair in pairs:
            t_id = pair.get("twitch_login")
            m_id = pair.get("mastodon_id")
            if not t_id or not m_id:
                continue
            if not t_id in map.keys():
                map[t_id] = []
            if not m_id in map[t_id]:
                map[t_id].append(m_id)
        return map

    def _commit_mt_map(self, map):
        self.l(DEBUG, "Running _commit_mt_map")
        for pair in self.custom_pairs:
            m_id = pair["mastodon_id"]
            t_id = pair["twitch_login"]
            if not m_id in map.keys():
                map[m_id] = []
            if not t_id in map[m_id]:
                map[m_id].append(t_id)
        self._bucket[self._m_to_t_path] = json.dumps(map)

    def _commit_tm_map(self, map):
        self.l(DEBUG, "Running _commit_tm_map")
        for pair in self.custom_pairs:
            t_id = pair["twitch_login"]
            m_id = pair["mastodon_id"]
            if not t_id in map.keys():
                map[t_id] = []
            if not m_id in map[t_id]:
                map[t_id].append(m_id)
        self._bucket[self._t_to_m_path] = json.dumps(map)

    def commit_maps(self, mt_map, tm_map):
        self.l(INFO, "Committing maps to s3 store.")
        self._commit_mt_map(map=mt_map)
        self._commit_tm_map(map=tm_map)
        self.refresh_maps()

    def refresh_maps(self):
        self.l(INFO, "Refreshing s3 maps.")
        try:
            del self.mt_map
        except AttributeError:
            pass
        try:
            del self.tm_map
        except AttributeError:
            pass
        try:
            del self.custom_pairs
        except AttributeError:
            pass
        try:
            del self.custom_mt_map
        except AttributeError:
            pass
        try:
            del self.custom_tm_map
        except AttributeError:
            pass

    def add_custom_pair(self, mastodon_id, twitch_login):
        self.l(INFO, "Adding custom pair.")
        try:
            pairs = json.loads(self._bucket[self._custom_pair_path])
        except ClientError:
            pairs = []
        new_pair = {
            "mastodon_id": mastodon_id,
            "twitch_login": twitch_login
        }
        for pair in pairs:
            if pair == new_pair:
                return False
        
        pairs.append(new_pair)
        self._bucket[self._custom_pair_path] = json.dumps(pairs)

    def del_custom_pair(self, mastodon_id, twitch_login):
        self.l(INFO, "Adding custom pair.")
        new_pairs = []
        try:
            pairs = json.loads(self._bucket[self._custom_pair_path])
        except ClientError:
            pairs = []
        del_pair = {
            "mastodon_id": mastodon_id,
            "twitch_login": twitch_login
        }
        for pair in pairs:
            if pair == del_pair:
                continue
            new_pairs.append(pair)
        
        self._bucket[self._custom_pair_path] = json.dumps(new_pairs)

    def commit_twitch_users(self, users):
        self.l(INFO, "Committing twitch users to s3 store.")
        self._bucket[self._twitch_user_path] = json.dumps(users)
        try:
            del self.twitch_users
        except AttributeError:
            pass