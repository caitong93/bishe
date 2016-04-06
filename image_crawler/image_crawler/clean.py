# -*- coding: utf8 -*-
import sys, os

import redis

sys.path.append(os.path.dirname(os.path.abspath('.')))
import image_crawler_settings

from scheduler import url_set, request_queue

if __name__ == '__main__':
    conn = redis.Redis(host=image_crawler_settings.redis_host, port=image_crawler_settings.redis_port)
    conn.delete(url_set)
    conn.delete(request_queue)
