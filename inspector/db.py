import feedparser
import time
import re
from inspector import config

bin_ttl = config.BIN_TTL
storage_backend = config.STORAGE_BACKEND

storage_module, storage_class = storage_backend.rsplit('.', 1)

try:
    klass = getattr(__import__(storage_module, fromlist=[storage_class]), storage_class)
except ImportError, e:
    raise ImportError("Unable to load storage backend '{}': {}".format(storage_backend, e))

db = klass(bin_ttl)


def create_bin(private=False, name=None):
    return db.create_bin(private, name)


def update_config(ttl=1000, count=50, prefix='PAYFORT'):
    return db.update_config(ttl, count, prefix)


def get_config():
    return db.get_config()


def delete_bin(name):
    return db.delete_bin(name)


def get_bin(name):
    return db.get_bin(name)


def update_bin(private=False, name=None, response_msg='ok\n', response_code=200, response_delay=0, requests=[],
               color=None, secret_key=None):
    return db.update_bin(private, name, response_msg, response_code, response_delay, requests, color, secret_key)


def create_request(bin, request):
    return db.create_request(bin, request)


def lookup_bin(name):
    name = re.split(r"[/.]", name)[0]
    return db.lookup_bin(name)


def bin_exist(name):
    name = re.split(r"[/.]", name)[0]
    return db.bin_exist(name)


def count_bins():
    return db.count_bins()


def get_bins():
    return db.get_bins()


def count_requests():
    return db.count_requests()


def avg_req_size():
    return db.avg_req_size()
