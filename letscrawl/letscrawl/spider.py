# -*- coding: utf8 -*-
import datetime
from urlparse import urlparse

import pymongo
from bs4 import BeautifulSoup

from crawler.utils import common_headers
from letscrawl import get_logger, image_crawler_settings
from core import Request, BaseItem, BaseSpider

logger = get_logger(__name__)


class ImageItem(BaseItem):
    db = pymongo.MongoClient(image_crawler_settings.MONGODB_URL)

    def __init__(self, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self._crawl_time = datetime.datetime.utcnow()

    def save(self):
        self.db['zol_desktop']['image'].insert_one(vars(self))


class Spider(BaseSpider):
    domain = ['http://desk.zol.com.cn', 'http://desk.fd.zol-img.com.cn']

    def start_urls(self):
        yield Request(method='GET', url='http://desk.zol.com.cn/',
                       headers=common_headers, callback=self.parse, meta={'depth': 3})

    def parse(self, response):
        # logger.info('[spider.parse] depth {}, url {}'.format(response.meta['depth'], response.url))

        soup = BeautifulSoup(response.body, 'lxml', from_encoding='gb2312')
        tags = soup.find_all(['a', 'img'])
        ret = []

        for tag in tags:
            try:
                if tag.name == 'a':
                    url_ = tag.get('href').strip()

                    if url_.startswith('/'): url_ = self.to_absolute(response.url, url_)

                    if self.url_filter(url_) and response.meta['depth'] < 1:
                        yield Request(method='GET',
                                      url=url_,
                                      headers=common_headers,
                                      callback=None,
                                      meta={'depth': response.meta['depth'] + 1})
                else:
                    src = ['loadsrc', 'srch', 'src']
                    found = False
                    for src_ in src:
                        if tag.has_attr(src_):
                            url_ = tag.get(src_).strip()

                            if url_.startswith('/'): url_ = self.to_absolute(response.url, url_)

                            # logger.warning(tag, url_)
                            if self.url_filter(url_): yield ImageItem(url=url_)

                            found = True
                            break
                    if not found: logger.warning('[spider.parse] Unknow img tag.')
            except Exception, e:
                logger.debug(u'tag string: {}'.format(unicode(tag)))
                logger.warning(e)

    def url_filter(self, url):
        for prefix in self.domain:
            if url.startswith(prefix): return True

        logger.warning('[spider.url_filter] Unkown domin: {}'.format(url))

        return False

    def to_absolute(self, url1, url2):
        res = urlparse(url1)
        return '://'.join([res.scheme, res.netloc]) + url2
