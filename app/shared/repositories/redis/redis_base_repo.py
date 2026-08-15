from datetime import timedelta

from redis import Redis


class RedisBaseRepository:
    def __init__(self, client: Redis):
        self.client = client

    async def get_instance(self, key: str) -> bytes | str | None:
        return await self.client.get(key)

    async def set_instance(
        self, key: str, value: bytes | str | None, expire_time: int | timedelta = None
    ) -> None:
        await self.client.set(name=key, value=value, ex=expire_time)

    async def delete_instance(self, key: str) -> None:
        await self.client.delete(key)

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

    async def check_existance(self, key: str) -> bool:
        return await self.client.exists(key) > 0
