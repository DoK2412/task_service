import redis.asyncio as redis
from setting import RedisData

class Redis(object):
    def __init__(self, host='redis', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, username=RedisData["user"], password=RedisData["password"])
