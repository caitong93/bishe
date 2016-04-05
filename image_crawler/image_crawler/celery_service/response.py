# -*- coding: utf8 -*-

class Response(object):
    def __init__(self, url, status, headers, body, callback=None, **kwargs):
        self.url = url
        self.status = status
        self.headers = headers
        self.body = body
        self.callback = callback

        for k, v in kwargs: setattr(self, k, v)

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