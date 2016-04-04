# -*- coding: utf8 -*-

class Request(object):
    def __init__(self, method, url, headers, callback=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.callback = callback

    def __unicode__(self):
        return '<Response> {} {}'.format(self.method, self.url)