import hashlib
import os
import json
import collections
import urllib
import datetime

import requests


cache_times = {}


def cached_get(url: str, max_age: datetime.timedelta) -> requests.Response:
    cache_dir = os.environ['WX_CACHE']

    url = urllib.parse.quote(url, safe='/:&?=%')

    url_hash = hashlib.sha3_256(url.encode('utf-8')).hexdigest()

    filename = cache_dir + '/' + url_hash

    now = datetime.datetime.now()

    if filename in cache_times and now - cache_times[filename] <= max_age:
        with open(filename) as f:
            text = f.read()

        ret = collections.namedtuple('Response', 'status_code url text json')

        ret.status_code = 200
        ret.url = url
        ret.text = text
        ret.json = lambda: json.loads(text)

        return ret

    r = requests.get(url)

    if r.status_code == 200 and r.url == url:
        with open(filename, 'w') as f:
            f.write(r.text)
        cache_times[filename] = now
    else:
        print(r.status_code, r.url, url)

    return r
