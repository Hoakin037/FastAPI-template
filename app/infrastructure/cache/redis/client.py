from redis.asyncio.client import Redis

from app.config.settings import RedisSettings


def create_redis_client(settings: RedisSettings):
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    )
