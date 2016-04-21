# -*- coding: utf8 -*-
import json
import time

import redis

import scheduler.tasks as sched_tasks
import spider
from crawler import tasks
from letscrawl import get_logger, image_crawler_settings
from scheduler import request_queue

redis_conn = redis.Redis(image_crawler_settings.redis_host, image_crawler_settings.redis_port)
spider_ = spider.Spider()
logger = get_logger(__name__)


def fetch_request(conn=redis_conn, q=request_queue):
    return conn.lpop(q)


for req in spider_.start_urls():
    sched_tasks.push.delay(req.to_dict())

countdown = 10
tot = 0
start = time.time()
timer = time.time()

while countdown:
    # Json string.
    request_dict = fetch_request()

    if request_dict is None:
        countdown -= 1
        # logger.info('[engine] Sleep for a while. countdown: {}.'.format(countdown))
        time.sleep(3)
        continue

    countdown = 10
    tot += 1

    # Dict object.
    request_dict = json.loads(request_dict)

    tasks.download.delay(request_dict)

    time.sleep(0.1)

    if time.time() > timer + 30: logger.info('{} requests per second, {} requests in total.'.format(int(tot/time.time() - start), tot))


logger.info('Total: {}'.format(tot))
# r = tasks.add.delay(1, 1)
# print r.get()