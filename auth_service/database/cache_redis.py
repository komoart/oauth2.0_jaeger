from typing import Awaitable

import redis
from aioredis import Redis

from core.settings import settings

redis_app = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db_int,
    decode_responses=True
)


class RedisStorage:
    def __init__(self, redis_conn: Redis):
        self.redis = redis_conn

    def get(self, key: str) -> Awaitable:
        return self.redis.get(key)

    def set(self, name: str, value: str, time: int) -> None:
        self.redis.setex(name, time, value)
        return None

    def delete(self, key: str) -> None:
        self.redis.delete(key)
