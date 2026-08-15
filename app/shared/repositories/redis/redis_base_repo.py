from datetime import timedelta

from redis import Redis


class RedisBaseRepository:
    def __init__(self, client: Redis):
        self.client = client

    def get_instance(self, key: str) -> bytes | str | None:
        return self.client.get(key)

    def set_instance(
        self, key: str, value: bytes | str | None, expire_time: int | timedelta = None
    ) -> None:
        self.client.set(name=key, value=value, ex=expire_time)

    def delete_instance(self, key: str) -> None:
        self.client.delete(key)

    def delete_by_prefix(self, prefix: str) -> None:
        cursor = b"0"
        pattern = f"{prefix}*"

        while cursor:
            cursor, keys = self.client.scan(
                cursor=int(cursor),
                match=pattern,
                count=50,
            )

            if keys:
                self.client.delete(*keys)

            if cursor == b"0":
                break

    def check_existance(self, key: str) -> bool:
        return self.client.exists(key) > 0
