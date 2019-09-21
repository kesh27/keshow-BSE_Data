import os

REDIS_HOST = os.environ.get('REDIS_HOST', '')
REDIS_PORT = os.environ.get('REDIS_PORT', '')
REDIS_DB_ID = os.environ.get('REDIS_DB_ID', '')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
APP_PORT = int(os.environ.get("PORT", 17995))
APP_HOST = int(os.environ.get("PORT", "127.0.0.1"))