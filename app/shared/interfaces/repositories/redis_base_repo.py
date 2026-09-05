from abc import ABC, abstractmethod
from datetime import timedelta


class IRedisBaseRepository(ABC):
    """
    Base interface for Redis repositories.

    Defines the minimal cache operations used by concrete Redis repositories.
    """

    @abstractmethod
    async def get_instance(self, key: str) -> bytes | str | None:
        """
        Get a cached value by key.

        :param key: Redis key.
        :return: Stored value or None when the key does not exist.
        """
        ...

    @abstractmethod
    async def set_instance(
        self, key: str, value: bytes | str | None, expire_time: int | timedelta = None
    ) -> None:
        """
        Store a value in Redis.

        :param key: Redis key.
        :param value: Value to store.
        :param expire_time: Optional TTL in seconds or as a timedelta.
        """
        ...

    @abstractmethod
    async def delete_instance(self, key: str) -> None:
        """
        Delete one cached value by key.

        :param key: Redis key to delete.
        """
        ...

    @abstractmethod
    async def delete_by_prefix(self, prefix: str) -> None:
        """
        Delete all cached values whose keys start with the given prefix.

        :param prefix: Redis key prefix.
        """
        ...

    @abstractmethod
    async def check_existence(self, key: str) -> bool:
        """
        Check whether a key exists in Redis.

        :param key: Redis key.
        :return: True when the key exists, otherwise False.
        """
        ...
