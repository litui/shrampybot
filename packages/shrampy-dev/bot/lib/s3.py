import os
import json
import logging
import tempfile
from base64 import b64encode, b64decode
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
        self._twitch_event_msg_id_path = "twitch_event_msg_ids"
        self._stream_cache_path = "stream_cache"
        self._channel_cache_path = "channel_cache"
        self._category_map_path = "category_map"
        self._stream_meta_path = "stream_meta"
        self._thumb_cache_path = "thumb_cache"

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

    @cached_property
    def stream_cache(self) -> dict:
        self.l(DEBUG, "Accessed stream_cache cached property.")
        try:
            streams = json.loads(self._bucket[self._stream_cache_path])
        except ClientError:
            self.l(WARN, "Accessed stream cache key before creation.")
            return {}
        return streams

    @cached_property
    def stream_meta(self) -> dict:
        self.l(DEBUG, "Accessed stream_meta cached property.")
        try:
            streams = json.loads(self._bucket[self._stream_meta_path])
        except ClientError:
            self.l(WARN, "Accessed stream meta key before creation.")
            return {}
        return streams

    @cached_property
    def channel_cache(self) -> dict:
        self.l(DEBUG, "Accessed channel_cache cached property.")
        try:
            streams = json.loads(self._bucket[self._channel_cache_path])
        except ClientError:
            self.l(WARN, "Accessed channel cache key before creation.")
            return {}
        return streams

    @cached_property
    def category_map(self) -> dict:
        self.l(DEBUG, "Accessed category_map cached property.")
        try:
            category_map = json.loads(self._bucket[self._category_map_path])
        except ClientError:
            self.l(WARN, "Accessed category map path before creation.")
            return {}
        return category_map

    def _commit_mt_map(self, map):
        self.l(DEBUG, "Running _commit_mt_map")
        mt_map = map.copy()
        for pair in self.custom_pairs:
            m_id = pair["mastodon_id"]
            t_id = pair["twitch_login"]
            if not m_id in mt_map.keys():
                mt_map[m_id] = []
            if not t_id in mt_map[m_id]:
                mt_map[m_id].append(t_id)
        self._bucket[self._m_to_t_path] = json.dumps(mt_map)

    def _commit_tm_map(self, map):
        self.l(DEBUG, "Running _commit_tm_map")
        tm_map = map.copy()
        for pair in self.custom_pairs:
            t_id = pair["twitch_login"]
            m_id = pair["mastodon_id"]
            if not t_id in tm_map.keys():
                tm_map[t_id] = []
            if not m_id in tm_map[t_id]:
                tm_map[t_id].append(m_id)
        self._bucket[self._t_to_m_path] = json.dumps(tm_map)

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

    def add_category(self, category_name, category_tags):
        self.l(INFO, "Adding category '{}' to category map.".format(
            category_name
        ))
        category_map = self.category_map.copy()
        category_map[category_name] = category_tags
        self.commit_category_map(category_map)

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

    def commit_category_map(self, category_map):
        self.l(INFO, "Committing category map to s3 store.")
        self._bucket[self._category_map_path] = json.dumps(category_map)
        try:
            del self.category_map
        except AttributeError:
            pass

    def check_and_stow_event_message_id(self, message_id, message={}):
        record_path = "/".join([
            self._twitch_event_msg_id_path,
            message_id
        ])
        matching_ids = self._bucket.list(prefix=record_path)
        if matching_ids:
            return True

        # If ID is new, record it as a key for later reference.
        key = self._bucket.key(record_path)
        if message:
            key.set(json.dumps(message))
        else:
            key.set(message_id)
        return False

    def stow_thumb_as_file(self, stream_id: str, binary_blob: bytes, extension="jpg"):
        self.l(INFO, "Stowing stream thumbnail for {}".format(stream_id))
        tmp_dir = tempfile.gettempdir()
        fd, filename = tempfile.mkstemp()
        with os.fdopen(fd, "bw") as f:
            f.write(binary_blob)
        thumb_key = self._bucket.key("/".join([
            self._thumb_cache_path,
            "{}.{}".format(stream_id, extension)
        ]))
        full_path = os.path.join(tmp_dir, filename)
        thumb_key.upload(full_path)
        os.remove(full_path)
        thumb_key.make_public()
        return thumb_key.url

    def update_stream_cache(self, channel_id: str, stream: dict):
        self.l(DEBUG, "Updating stream cache for channel id {}" \
            .format(channel_id)
        )
        streams = self.stream_cache.copy()
        # simply replace existing, if any.
        streams[channel_id] = stream
        self._bucket[self._stream_cache_path] = json.dumps(streams)

        try:
            del self.stream_cache
        except AttributeError:
            pass

        return True

    def update_stream_meta(self, channel_id: str, channel_meta: dict):
        self.l(DEBUG, "Updating stream metadata for channel id {}" \
            .format(channel_id)
        )
        streams = self.stream_meta.copy()
        # simply replace existing, if any.
        streams[channel_id] = channel_meta
        self._bucket[self._stream_meta_path] = json.dumps(streams)

        try:
            del self.stream_meta
        except AttributeError:
            pass

        return True

    def update_channel_cache(self, channel_id: str, channel: dict):
        self.l(DEBUG, "Updating channel cache for channel id {}" \
            .format(channel_id)
        )
        channels = self.channel_cache.copy()
        # simply replace existing, if any.
        channels[channel_id] = channel
        self._bucket[self._channel_cache_path] = json.dumps(channels)

        try:
            del self.channel_cache
        except AttributeError:
            pass

        return True


class CachedDataRetrievalError(ClientError):
    pass