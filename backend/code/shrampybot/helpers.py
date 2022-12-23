import re

def chunkify_list(input_list, count=100):
    for i in range(0, len(input_list), count):
        yield input_list[i:i + count]

def get_twitch_id_from_url(url):
    res = re.findall(
        pattern=r"\"(?:https?:\/\/)?(?:www\.)?twitch\.tv\/([A-Za-z0-9_-]+)\/?\"",
        string=url,
        flags=re.I
    )
    if len(res) == 1:
        return res[0].lower()
    else:
        # Without quotes.
        res = re.findall(
            pattern=r"(?:https?:\/\/)?(?:www\.)?twitch\.tv\/([A-Za-z0-9_-]+)\/?",
            string=url,
            flags=re.I
        )
        if len(res) == 1:
            return res[0].lower()