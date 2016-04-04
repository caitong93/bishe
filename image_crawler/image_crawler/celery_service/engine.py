# -*- coding: utf8 -*-
import redis

from celery_service import image_crawler_settings
from celery_service import tasks
import scheduler.tasks as sched_tasks

redis_conn = redis.Redis(image_crawler_settings.redis_host, image_crawler_settings.redis_port)


while True:
    request = redis_conn.lpop(request_queue)
