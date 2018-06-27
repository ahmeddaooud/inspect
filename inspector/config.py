import os, urlparse
DEBUG = False
REALM = os.environ.get('REALM', 'local')

ROOT_URL = "http://localhost:4000"

PORT_NUMBER = 4000

ENABLE_CORS = False
CORS_ORIGINS = "*"

FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "N1BKhJLnBqLpexOZdklsfDKFJDKFadsfs9a3r324YB7B73AglRmrHMDQ9RhXz35")

BIN_TTL = 48*3600
STORAGE_BACKEND = "inspector.storage.memory.MemoryStorage"
MAX_RAW_SIZE = int(os.environ.get('MAX_RAW_SIZE', 1024*10))
IGNORE_HEADERS = ["X-Via", "X-Varnish", "X-Heroku-Dynos-In-Use", "X-Heroku-Queue-Depth", "X-Request-Start", "X-Forwarded-Port", "X-Request-Id", "X-Forwarded-Proto", "X-Forwarded-For", "Content-Length", "Accept-Encoding", "Connection", "Accept", "Cache-Control", "Postman-Token", "User-Agent", "Accept-Language", "Upgrade-Insecure-Requests", "Cookie", "Host", "Origin"]
MAX_REQUESTS = 50
CLEANUP_INTERVAL = 8*3600

REDIS_URL = ""
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 9

REDIS_PREFIX = "inspector"

BUGSNAG_KEY = ""

if REALM == 'prod':
    DEBUG = False
    ROOT_URL = "https://payfort-inspector.herokuapp.com"

    FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", FLASK_SESSION_SECRET_KEY)

    STORAGE_BACKEND = "STORAGE_BACKEND = "redis://h:pe77b1fcde5d48244133f41796a93944829bf4070e87af0b6adb01ed53f67f3b8@ec2-54-236-163-73.compute-1.amazonaws.com:25699"

    REDIS_URL = os.environ.get("REDIS_URL")
    url_parts = urlparse.urlparse(REDIS_URL)
    REDIS_HOST = url_parts.hostname
    REDIS_PORT = url_parts.port
    REDIS_PASSWORD = url_parts.password
    REDIS_DB = url_parts.fragment

    BUGSNAG_KEY = os.environ.get("BUGSNAG_KEY", BUGSNAG_KEY)

    IGNORE_HEADERS = """
X-Varnish
X-Forwarded-For
X-Heroku-Dynos-In-Use
X-Request-Start
X-Heroku-Queue-Wait-Time
X-Heroku-Queue-Depth
X-Real-Ip
X-Forwarded-Proto
X-Via
X-Forwarded-Port
""".split("\n")[1:-1]
