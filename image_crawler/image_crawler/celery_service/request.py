# -*- coding: utf8 -*-
import json


class Request(object):
    def __init__(self, method=None, url=None, headers=None, callback=None):
        self.method = method
        self.url = url
        self.headers = headers

        # 可以使用string形式的函数名, 或者直接传递一个Spider中的method
        if isinstance(callback, str) or isinstance(callback, unicode):
            self.callback = callback
        elif hasattr(callback, '__name__'):
            self.callback = callback.__name__
        else:
            raise Exception(u'callback must be string or method of spider.')

    def __repr__(self):
        json_dumps = json.dumps(vars(self), ensure_ascii=False, encoding='utf-8', indent=4)
        # print json_dumps
        return json_dumps

    def __unicode__(self):
        return '<Response> {} {}'.format(self.method, self.url)

    def to_dict(self):
        return vars(self)

    @staticmethod
    def load(d):
        return Request(**d)
