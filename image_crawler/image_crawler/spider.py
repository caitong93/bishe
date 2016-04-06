# -*- coding: utf8 -*-

from bs4 import BeautifulSoup

from crawler.utils import common_headers
from image_crawler import get_logger
from core import Request, BaseItem, BaseSpider

logger = get_logger(__name__)


class DummyItem(BaseItem):
    pass


class Spider(BaseSpider):
    domain = 'http://desk.zol.com.cn'

    def start_urls(self):
        yield Request(method='GET', url='http://desk.zol.com.cn/',
                       headers=common_headers, callback=self.parse, meta={'depth': 0})

    def parse(self, response):
        logger.info('[spider.parse] depth {}, url {}'.format(response.meta['depth'], response.url))

        soup = BeautifulSoup(response.body, 'lxml', from_encoding='gb2312')
        tags = soup.find_all(['a', 'img'])
        ret = []

        for tag in tags:
            try:
                if tag.name == 'a':
                    url_ = tag.get('href').strip()

                    if url_.startswith('/'): url_ = self.domain + url_

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

                            if url_.startswith('/'): url_ = self.domain + url_

                            if self.url_filter(url_): yield DummyItem()

                            found = True
                            break
                    if not found: logger.warning('[spider.parse] Unknow img tag.')
            except Exception, e:
                logger.warning(e)
                logger.info(u'tag string: {}'.format(unicode(tag)))


    def url_filter(self, url):
        return  url.startswith('http://desk.zol.com.cn')
