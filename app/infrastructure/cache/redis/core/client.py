from redis import Redis
from settings.redis import RedisSettings
from starlette.requests import Request


def create_redis_client(settings: RedisSettings):
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    )


async def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis()
