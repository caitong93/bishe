# -*- coding: utf8 -*-
from __future__ import absolute_import

import time
import sys
import os

import redis
import requests
from celery import Task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from crawler.celery import app
from crawler import storage, image_crawler_settings
import scheduler.tasks as sched_tasks
from core import Response, Request
from spider import Spider


# +++++++++ Item Pipeline
class ItemTask(Task):
    abstract = True
    ignore_result = True


@app.task(base=ItemTask)
def item_pipeline(item):
    item.save()

# +++++++++ Parser

class SpiderTask(Task):
    abstract = True
    ignore_result = True
    _spider = Spider()

    def after_return(self, *args, **kwargs):
        pass


@app.task(base=SpiderTask)
def parse(response):
    _spider = parse._spider
    if response.callback and hasattr(_spider, response.callback):
        _parse = getattr(_spider, response.callback)
        try:
            for res in _parse(response):
                if isinstance(res, Request):
                    logger.debug('[parse] Request: {}'.format(unicode(res)))
                    sched_tasks.push.delay(res.to_dict())
                else:
                    logger.debug('[parse] Item')
                    item_pipeline.delay(res)

        except TypeError:
            pass


# +++++++++ Downloader
class DownloadTask(Task):
    abstract = True
    ignore_result = True

    def after_return(self, status, retval, *args, **kwargs):
        if isinstance(retval, Response):
            parse.delay(retval)


@app.task(base=DownloadTask, retry=True, countdown=3)
def download(request):
    # Get Request object.
    request = Request.load(request)

    # todo: 目前只支持 GET
    if request.method == 'GET':
        try:
            r = requests.get(request.url, headers=request.headers, timeout=10.0)
            logger.debug('[download] {} {} {}'.format(request.method, r.status_code, request.url))
            if r.status_code == 200:
                return Response(url=request.url, status=r.status_code, headers=r.headers, body=r.content, callback=request.callback,
                                method=request.method, meta=request.meta)
            else:
                logger.critical('[download] HTTP code error: {}'.format(r.status_code))
        except Exception, e:
            raise e
    else:
        raise Exception('The {} method is not implemented now.'.format(request.method))


@app.task
def add(x, y):
    return x + y