from redis import Redis
from starlette.requests import Request

from app.config.settings import RedisSettings


def create_redis_client(settings: RedisSettings):
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    )


async def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis()
