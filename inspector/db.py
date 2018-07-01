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

def create_bin(private=False):
    return db.create_bin(private)

def delete_bin(name):
    return db.delete_bin(name)

def create_request(bin, request):
    return db.create_request(bin, request)

def lookup_bin(name):
    name=re.split(r"[/.]", name)[0]
    return db.lookup_bin(name)

def bin_exist(name):
    name=re.split(r"[/.]", name)[0]
    return db.bin_exist(name)

def count_bins():
    return db.count_bins()

def get_bins():
    return db.get_bins()

def count_requests():
    return db.count_requests()

def avg_req_size():
    return db.avg_req_size()
