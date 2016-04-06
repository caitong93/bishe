# -*- coding: utf8 -*-
import json


class Request(object):
    def __init__(self, method=None, url=None, headers=None, callback=None, meta=None):
        self.method = method
        self.url = url
        self.headers = headers

        # 可以使用string形式的函数名, 或者直接传递一个Spider中的method
        if callback:
            if isinstance(callback, str) or isinstance(callback, unicode):
                self.callback = callback
            elif hasattr(callback, '__name__'):
                self.callback = callback.__name__
            else:
                raise Exception(u'callback {} must be string or method of spider.'.format(callback))
        else:
            self.callback = None

        # meta 只支持简单的 Python 对象
        self.meta = meta

    def __repr__(self):
        json_dumps = json.dumps(vars(self), ensure_ascii=False, encoding='utf-8', indent=4)
        # print json_dumps
        return json_dumps

    def __unicode__(self):
        return '<Request> {} {}'.format(self.method, self.url)

    def to_dict(self):
        return vars(self)

    @staticmethod
    def load(d):
        return Request(**d)


class Response(object):
    """
    def __init__(self, url, status, headers, body, callback=None, **kwargs):
        self.url = url
        self.status = status
        self.headers = headers
        self.body = body
        self.callback = callback

        for k, v in kwargs: setattr(self, k, v)
    """
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)

    def __unicode__(self):
        if hasattr(self, 'method'):
            return '<Response> {} {} {}'.format(self.method, self.status, self.url)
        else:
            return '<Response> {} {}'.format(self.status, self.url)

    def to_dict(self):
        return vars(self)

    @staticmethod
    def load(d):
        return Response(**d)


class BaseSpider(object):
    pass


class BaseItem(object):
    pass