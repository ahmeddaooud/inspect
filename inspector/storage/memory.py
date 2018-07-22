import time
import operator

from ..models import Bin

from inspector import config

class MemoryStorage():
    cleanup_interval = config.CLEANUP_INTERVAL

    def __init__(self, bin_ttl):
        self.bin_ttl = bin_ttl
        self.bins = {}
        self.request_count = 0

    def do_start(self):
        self.spawn(self._cleanup_loop)

    def _cleanup_loop(self):
        while True:
            self.async.sleep(self.cleanup_interval)
            self._expire_bins()

    def _expire_bins(self):
        expiry = time.time() - self.bin_ttl
        for name, bin in self.bins.items():
            if bin.created < expiry:
                self.bins.pop(name)

    def create_bin(self, private=False, name=None):
        bin = Bin(private, name)
        self.bins[bin.name] = bin
        return self.bins[bin.name]

    def update_bin(self, private=False, name=None, response_msg='ok\n', response_code=200, response_delay=0, requests=[], color=None, secret_key=None):
        bin = Bin(private, name, response_msg, response_code, response_delay, requests, color, secret_key)
        self.bins[bin.name] = bin
        return self.bins[bin.name]

    def delete_bin(self, name):
           self.bins.pop(name)

    def create_request(self, bin, request):
        bin.add(request)
        self.request_count += 1

    def count_bins(self):
        return len(self.bins)

    def get_bins(self):
        return sorted(self.bins)

    def get_bin(self, name):
        return self.bins[name]
    def count_requests(self):
        return self.request_count

    def avg_req_size(self):
        return None

    def lookup_bin(self, name):
        return self.bins[name]

    def bin_exist(self, name):
        try:
            self.bins[name]
            return True
        except:
            return False
