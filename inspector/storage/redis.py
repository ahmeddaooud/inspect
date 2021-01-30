from __future__ import absolute_import

import redis

from inspector import config
from ..models import Bin


class RedisStorage():
    prefix = config.REDIS_PREFIX

    def __init__(self, bin_ttl):
        self.bin_ttl = bin_ttl
        self.redis = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB,
                                       password=config.REDIS_PASSWORD)

    def _key(self, name):
        return '{}_{}'.format(self.prefix, name)

    def _request_count_key(self):
        return '{}-requests'.format(self.prefix)

    def _configurations(self):
        return '{}-configurations'.format(self.prefix)

    def create_bin(self, private=False, name=None, ):
        bin = Bin(private, name)
        key = self._key(bin.name)
        self.redis.set(key, bin.dump())
        self.redis.expireat(key, int(bin.created + self.bin_ttl))
        return bin

    def update_bin(self, private=False, name=None, response_msg='ok', response_code=200, response_delay=0,
                   requests=[], color=None, secret_key=None):
        bin = Bin(private, name, response_msg, response_code, response_delay, requests, color, secret_key)
        key = self._key(bin.name)
        self.redis.set(key, bin.dump())
        self.redis.expireat(key, int(bin.created + self.bin_ttl))
        return bin

    def delete_bin(self, name):
        key = self._key(name)
        self.redis.delete(key)

    def create_request(self, bin, request):
        bin.add(request)
        key = self._key(bin.name)
        self.redis.set(key, bin.dump())
        self.redis.expireat(key, int(bin.created + self.bin_ttl))

        self.redis.setnx(self._request_count_key(), 0)
        self.redis.incr(self._request_count_key())

    def update_config(self, ttl, count, prefix):
        try:
            self.redis.set(self._configurations(), ttl+', '+count+', '+prefix)
        except TypeError:
            self.redis.set(self._configurations(), '604800, 50, PAYFORT')

    def get_config(self):
        config = self._configurations()
        serialized_config = self.redis.get(config)
        config_list = serialized_config.split(', ')
        return config_list

    def count_bins(self):
        keys = self.redis.keys("{}_*".format(self.prefix))
        return len(keys)

    def get_bins(self):
        bins = []
        keys = self.redis.keys("{}_*".format(self.prefix))
        for key in keys:
            serialized_bin = self.redis.get(key)
            try:
                bin = Bin.load(serialized_bin)
                bins.append(bin)
            except TypeError:
                self.redis.delete(key)  # clear bad data
        return bins

    def get_bin(self, name):
        key = self._key(name)
        serialized_bin = self.redis.get(key)
        try:
            bin = Bin.load(serialized_bin)
            return bin
        except TypeError:
            raise Exception('Bin Not Found')

    def count_requests(self):
        return int(self.redis.get(self._request_count_key()) or 0)

    def avg_req_size(self):
        info = self.redis.info()
        return info['used_memory'] / info['db0']['keys'] / 1024

    def lookup_bin(self, name):
        key = self._key(name)
        serialized_bin = self.redis.get(key)
        try:
            bin = Bin.load(serialized_bin)
            return bin
        except TypeError:
            self.redis.delete(key)  # clear bad data
            raise KeyError("Bin not found")

    def bin_exist(self, name):
        key = self._key(name)
        serialized_bin = self.redis.get(key)
        try:
            Bin.load(serialized_bin)
            return True
        except TypeError:
            return False
