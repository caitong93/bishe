# -*- coding: utf8 -*-
from __future__ import absolute_import

import hashlib

import redis
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from scheduler.celery import app
from scheduler import image_crawler_settings

url_set = 'url_set'
request_queue = 'request_queue'


class ScheTask(app.Task):
    abstract = True
    ignore_result = True

    # Scheduler 和 请求队列所在的 Redis 运行在同一个 Host 上
    _redis_conn = None

    @property
    def redis_conn(self):
        if self._redis_conn is None:
            self._redis_conn = redis.Redis(image_crawler_settings.redis_host, image_crawler_settings.redis_port)
            # 清理
            self._redis_conn.delete(url_set)
            self._redis_conn.delete(request_queue)

        return self._redis_conn


@app.task(base=ScheTask)
def push(request):
    hashval = md5(request.url)
    conn = push.redis_conn

    if not conn.sismember(url_set, hashval):
        conn.sadd(url_set, hashval)
        conn.rpush(request_queue, request)


@app.task(base=ScheTask)
def pop():
    conn = pop.redis_conn
    return conn.lpop(request_queue)


@app.task
def add(x, y):
    return x + y


# +++++++++ helper functions


def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()
