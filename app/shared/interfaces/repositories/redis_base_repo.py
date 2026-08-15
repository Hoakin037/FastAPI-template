from datetime import timedelta

from redis import Redis


class RedisBaseRepository:
    def __init__(self, client: Redis):
        self.client = client

    def get_instance(self, key: str) -> bytes | str | None: ...

    def set_instance(
        self, key: str, value: bytes | str | None, expire_time: int | timedelta = None
    ) -> None: ...

    def delete_instance(self, key: str) -> None:
        self.client.delete(key)

    def delete_by_prefix(self, prefix: str) -> None: ...

    def check_existance(self, key: str) -> bool: ...
