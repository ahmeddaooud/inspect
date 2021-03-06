import os
import urlparse

DEBUG = True
REALM = os.environ.get('REALM', 'local')

ROOT_URL = "http://localhost:4000"
PORT_NUMBER = 4000

ENABLE_CORS = False
CORS_ORIGINS = "*"

FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "N1CKImLnBqLpexOZpkisfDKFJDKFadsfs8a3r324YB7B73AglRmrHMDQ9RhXz35")
SESSION_COOKIE_SAMESITE = "None"

BIN_TTL = 2*168*3600
STORAGE_BACKEND = "inspector.storage.memory.MemoryStorage"
MAX_RAW_SIZE = int(os.environ.get('MAX_RAW_SIZE', 1024*10))
IGNORE_HEADERS = ["X-Heroku-Dynos-In-Use", "X-Heroku-Queue-Depth"]
MAX_REQUESTS = 500
CLEANUP_INTERVAL = 12*3600

REDIS_URL = ""
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 9
REDIS_PREFIX = ""

DATABASE_URL = "sqlite:///inspector.db"

BUGSNAG_KEY = ""

if REALM == 'prod':
    DEBUG = False
    ROOT_URL = "https://inspect-payfort.herokuapp.com"

    FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", FLASK_SESSION_SECRET_KEY)
    SESSION_COOKIE_SAMESITE = "None"
    STORAGE_BACKEND = "inspector.storage.redis.RedisStorage"

    REDIS_URL = os.environ.get("REDISCLOUD_URL")
    url_parts = urlparse.urlparse(REDIS_URL)
    REDIS_HOST = url_parts.hostname
    REDIS_PORT = url_parts.port
    REDIS_PASSWORD = url_parts.password
    REDIS_DB = url_parts.fragment

#     DATABASE_URL = "sqlite:///inspector.db"
    DATABASE_URL = "mysql+pymysql://obng2piq7zuprsa5:icshcyhiqvctkje3@fojvtycq53b2f2kx.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/qcwbp1tvcky5cpf1"

    BUGSNAG_KEY = os.environ.get("BUGSNAG_KEY", BUGSNAG_KEY)

    IGNORE_HEADERS = ["X-Heroku-Dynos-In-Use", "X-Heroku-Queue-Depth"]
