from datetime import timedelta

from redis.asyncio.client import Redis

from app.infrastructure.decorators import logg_function
from app.infrastructure.logger import setup_logging


class RedisBaseRepository:
    def __init__(self, client: Redis):
        self.client = client
        self._logger = setup_logging(__name__)

    @logg_function(description="Get instance from redis by key")
    async def get_instance(self, key: str) -> bytes | str | None:
        return await self.client.get(key)

    @logg_function(description="Set instance to redis")
    async def set_instance(
        self, key: str, value: bytes | str | None, expire_time: int | timedelta = None
    ) -> None:
        await self.client.set(name=key, value=value, ex=expire_time)

    @logg_function(description="Delete instance from redis by key")
    async def delete_instance(self, key: str) -> None:
        await self.client.delete(key)

    @logg_function(description="Delete instance from redis by prefix")
    async def delete_by_prefix(self, prefix: str) -> None:
        cursor = b"0"
        pattern = f"{prefix}*"

        while cursor:
            cursor, keys = await self.client.scan(
                cursor=int(cursor),
                match=pattern,
                count=50,
            )

            if keys:
                await self.client.delete(*keys)

            if cursor == b"0":
                break

    @logg_function(description="Check instance existence in redis")
    async def check_existence(self, key: str) -> bool:
        return await self.client.exists(key) > 0
