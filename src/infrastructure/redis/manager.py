from contextlib import contextmanager

import redis

from src.common.core.config import settings


class RedisManager:
    _instances = {}

    @classmethod
    def get_instance(cls, redis_id):
        if redis_id not in cls._instances:
            cls._instances[redis_id] = cls(redis_id)
        return cls._instances[redis_id]

    def __init__(self, redis_id):
        self.redis_id = redis_id
        self._pool = redis.ConnectionPool.from_url(
            f"redis://{settings.REDIS_HOSTS[redis_id]['HOST']}:{settings.REDIS_HOSTS[redis_id]['PORT']}/{settings.REDIS_HOSTS[redis_id]['DB']}",
            password=settings.REDIS_HOSTS[redis_id].get('PASSWORD'),
            decode_responses=True
        )

    @contextmanager
    def get_client(self):
        client = redis.Redis(connection_pool=self._pool)
        try:
            yield client
        finally:
            client.close()


def get_redis_manager(redis_id='default'):
    return RedisManager.get_instance(redis_id)


"""
with self.redis_manager.get_redis_client() as redis_client:
    ...
"""