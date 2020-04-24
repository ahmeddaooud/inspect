import copy
import datetime
import json
import os
import time

import msgpack

from inspector import config
from .util import random_color
from .util import solid16x16gif_datauri
from .util import tinyid


class Bin(object):
    max_requests = config.MAX_REQUESTS

    def __init__(self, private=False, name=None, response_msg='ok', response_code=200, response_delay=0,
                 requests=[], color=None, secret_key=None):
        self.created = time.time()
        self.private = private
        if color is None:
            self.color = random_color()
        else:
            self.color = color
        self.name = name
        self.response_msg = response_msg
        self.response_code = response_code
        self.response_delay = response_delay
        self.favicon_uri = solid16x16gif_datauri(*self.color)
        self.requests = requests
        if secret_key is None:
            self.secret_key = os.urandom(24) if self.private else None
        else:
            self.secret_key = secret_key

    def json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return dict(
            private=self.private,
            color=self.color,
            response_msg=self.response_msg,
            response_code=self.response_code,
            response_delay=self.response_delay,
            name=self.name,
            request_count=self.request_count)

    def dump(self):
        o = copy.copy(self.__dict__)
        o['requests'] = [r.dump() for r in self.requests]
        return msgpack.dumps(o)

    @staticmethod
    def load(data):
        o = msgpack.loads(data)
        o['requests'] = [Request.load(r) for r in o['requests']]
        b = Bin()
        b.__dict__ = o
        return b

    @property
    def request_count(self):
        return len(self.requests)

    def add(self, request):
        self.requests.insert(0, Request(request))
        if len(self.requests) > self.max_requests:
            for _ in xrange(self.max_requests, len(self.requests)):
                self.requests.pop(self.max_requests)


class Request(object):
    ignore_headers = config.IGNORE_HEADERS
    max_raw_size = config.MAX_RAW_SIZE

    def __init__(self, input=None):
        if input:
            self.id = tinyid(6)
            self.time = time.time()
            self.remote_addr = input.headers.get('X-Forwarded-For', input.remote_addr)
            self.method = input.method
            self.headers = dict(input.headers)

            for header in self.ignore_headers:
                self.headers.pop(header, None)

            self.query_string = input.args.to_dict(flat=True)
            self.form_data = []

            for k in input.form:
                self.form_data.append([k, input.values[k]])

            self.body = input.data
            self.path = input.path
            self.content_type = self.headers.get("Content-Type", "")

            self.raw = input.environ.get('raw')
            self.content_length = len(self.raw)
            if self.raw and len(self.raw) > self.max_raw_size:
                self.raw = self.raw[0:self.max_raw_size]

    def json(self):
        return json.dumps(self.to_dict())
    
    def to_dict(self):
        return dict(
            id=self.id,
            time=self.time,
            remote_addr=self.remote_addr,
            method=self.method,
            headers=self.headers,
            query_string=self.query_string,
            raw=self.raw,
            form_data=self.form_data,
            body=self.body,
            path=self.path,
            content_length=self.content_length,
            content_type=self.content_type,
        )

    @property
    def created(self):
        return datetime.datetime.fromtimestamp(self.time)

    def dump(self):
        return msgpack.dumps(self.__dict__)

    @staticmethod
    def load(data):
        r = Request()
        try:
            r.__dict__ = msgpack.loads(data, encoding="utf-8")
        except UnicodeDecodeError:
            r.__dict__ = msgpack.loads(data, encoding="ISO-8859-1")

        return r
