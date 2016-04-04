# -*- coding: utf8 -*-
import os
import time

from bs4 import BeautifulSoup

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from celery_service import image_crawler_settings
from celery_service.celery import app
from celery_service.response import Response
from celery_service.request import Request
from celery_service.utils import common_headers


class DummyItem(object):
    pass


class Spider(object):
    def start_urls(self):
        return Request(method='GET', url='http://desk.zol.com.cn/',
                       headers=common_headers, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='gb2312')
        tags = soup.find_all(['a', 'img'])
        ret = []

        for tag in tags:
            try:
                if tag.name == 'a':
                    url_ = tag.get('href').strip()

                    if self.url_filter(url_):
                        yield Request(method='GET', url=url_,
                                      # todo:实现meta
                                      headers=common_headers, callback=None)
                else:
                    src = ['loadsrc', 'srch', 'src']
                    found = False
                    for src_ in src:
                        if tag.has_attr(src_):
                            url_ = tag.get(src_).strip()

                            if self.url_filter(url_):
                                yield DummyItem()

                            found = True
                            break
                    if not found: raise Exception('unknow img tag')
            except Exception, e:
                logger.warning(e)
                logger.info(u'tag string: {}'.format(unicode(tag)))


    def url_filter(url):
        return url.startswith('/') or url.startswith('http://desk.zol.com.cn')
