import json

import redis

from scheduler import url_set, request_queue

conn = redis.Redis()


def fetch_request(conn=conn, q=request_queue):
    return conn.lpop(q)

while conn.llen(request_queue):
    # Json string.
    request_dict = fetch_request()

    if request_dict is None:
        countdown -= 1
        continue

    countdown = 10

    # Dict object.
    request_dict = json.loads(request_dict)