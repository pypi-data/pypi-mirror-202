import os

import redis.asyncio as redis

_host = os.getenv('REDIS_HOST', 'redis')
redis_client = redis.Redis(host=_host)
