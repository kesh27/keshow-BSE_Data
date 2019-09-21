import os

REDIS_HOST = os.environ.get('REDIS_HOST', '')
REDIS_PORT = os.environ.get('REDIS_PORT', '')
REDIS_DB_ID = os.environ.get('REDIS_DB_ID', '')