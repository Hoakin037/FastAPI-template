from redis.asyncio import Redis
from starlette.requests import Request


async def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis()
