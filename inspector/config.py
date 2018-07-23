import os, urlparse
DEBUG = True
REALM = os.environ.get('REALM', 'local')

ROOT_URL = "http://localhost:4000"

PORT_NUMBER = 4000

ENABLE_CORS = False
CORS_ORIGINS = "*"

FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "N1CKImLnBqLpexOZpkisfDKFJDKFadsfs8a3r324YB7B73AglRmrHMDQ9RhXz35")
SESSION_COOKIE_SAMESITE = "Strict"

BIN_TTL = 168*3600
STORAGE_BACKEND = "inspector.storage.memory.MemoryStorage"
MAX_RAW_SIZE = int(os.environ.get('MAX_RAW_SIZE', 1024*10))
IGNORE_HEADERS = ["X-Via", "Via", "X-Varnish", "X-Heroku-Dynos-In-Use", "X-Heroku-Queue-Depth", "X-Request-Start", "X-Forwarded-Port", "X-Request-Id", "X-Forwarded-Proto", "X-Forwarded-For", "Content-Length", "Accept-Encoding", "Connection", "Accept", "Cache-Control", "Postman-Token", "User-Agent", "Accept-Language", "Upgrade-Insecure-Requests", "Cookie", "Host", "Origin"]
MAX_REQUESTS = 100
CLEANUP_INTERVAL = 12*3600

REDIS_URL = ""
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 9

REDIS_PREFIX = ""

BUGSNAG_KEY = ""

if REALM == 'prod':
    DEBUG = False
    ROOT_URL = "https://payfort-inspector.herokuapp.com"

    FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", FLASK_SESSION_SECRET_KEY)
    SESSION_COOKIE_SAMESITE = "Strict"
    STORAGE_BACKEND = "inspector.storage.redis.RedisStorage"

    REDIS_URL = os.environ.get("REDIS_URL")
    url_parts = urlparse.urlparse(REDIS_URL)
    REDIS_HOST = url_parts.hostname
    REDIS_PORT = url_parts.port
    REDIS_PASSWORD = url_parts.password
    REDIS_DB = url_parts.fragment

    BUGSNAG_KEY = os.environ.get("BUGSNAG_KEY", BUGSNAG_KEY)

    IGNORE_HEADERS = ["X-Via", "Via", "X-Varnish", "X-Heroku-Dynos-In-Use", "X-Heroku-Queue-Depth", "X-Request-Start",
                      "X-Forwarded-Port", "X-Request-Id", "X-Forwarded-Proto", "X-Forwarded-For", "Content-Length",
                      "Accept-Encoding", "Connection", "Accept", "Cache-Control", "Postman-Token", "User-Agent",
                      "Accept-Language", "Upgrade-Insecure-Requests", "Cookie", "Host", "Origin"]
