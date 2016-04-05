# -*- coding: utf8 -*-
from __future__ import absolute_import

import time
import sys
import os

import redis
import requests
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from celery_service.celery import app
from celery_service import storage, image_crawler_settings
from celery_service.response import Response
from celery_service.request import Request
from spider import Spider


"""
@app.task
def download(url):
    r = requests.get(url, headers=common_headers, timeout=5.0)
    if r.status_code == 200:
        file_name = url.split('/')[-1]
        save_to_path = os.path.join(storage, file_name)
        with open(save_to_path, 'w') as f:
            f.write(r.content)
"""

# +++++++++ Parser

class SpiderTask(app.Task):
    abstract = True
    ignore_result = True
    _spider = Spider()
    _redis_conn = redis.Redis(image_crawler_settings.redis_host, image_crawler_settings.redis_port)

    def after_return(self, *args, **kwargs):
        pass


@app.task(base=SpiderTask)
def parse(response):
    response = Response.load(response)

    _spider = parse._spider
    if response.callback and hasattr(_spider, response.callback):
        _parse = getattr(_spider, response.callback)
        try:
            for res in _parse(response):
                if isinstance(res, Request):
                    logger.info('[parse] get Request: {}'.format(unicode(res)))
                else:
                    logger.info('[parse] get Item')

        except TypeError:
            pass

# +++++++++ Downloader

class DownloadTask(app.Task):
    abstract = True
    ignore_result = True

    def after_return(self, *args, **kwargs):
        res = args[1]
        parse.delay(res)


@app.task(base=DownloadTask)
def download(request):
    request = Request.load(request)

    # todo: 目前只支持 GET
    if request.method == 'GET':
        try:
            r = requests.get(request.url, headers=request.headers, timeout=5.0)
            if r.status_code == 200:
                return Response(url=request.url, status=r.status_code, headers=r.headers, body=r.content, callback=request.callback,
                                method=request.method).to_dict()
            else:
                raise Exception('[download] HTTP code error: {}'.format(r.status_code))
        except Exception, e:
            raise e
    else:
        raise Exception('The method is not implemented now.')


@app.task
def add(x, y):
    return x + y