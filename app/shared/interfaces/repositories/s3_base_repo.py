from abc import ABC, abstractmethod


class IS3BaseRepository(ABC):
    """
    Base interface for S3-compatible object storage repositories.

    Defines common object operations used by storage-backed modules.
    """

    @abstractmethod
    async def put_object(self, bucket_name: str, key: str, data: bytes) -> str:
        """
        Upload bytes to an object storage bucket.

        :param bucket_name: Target bucket name.
        :param key: Object key inside the bucket.
        :param data: Binary object content.
        :return: Stored object key.
        """
        ...

    @abstractmethod
    async def get_object(self, bucket_name: str, key: str) -> bytes:
        """
        Download object bytes from a bucket.

        :param bucket_name: Source bucket name.
        :param key: Object key inside the bucket.
        :return: Binary object content.
        """
        ...

    @abstractmethod
    async def get_head_object(self, bucket: str, key: str) -> dict:
        """
        Read object metadata from a bucket.

        :param bucket: Source bucket name.
        :param key: Object key inside the bucket.
        :return: Object metadata dictionary.
        """
        ...

    @abstractmethod
    async def get_objects_batch(
        self, bucket_name: str, keys: list[str]
    ) -> dict[str, bytes]:
        """
        Download multiple objects concurrently.

        :param bucket_name: Source bucket name.
        :param keys: Object keys to download.
        :return: Mapping of successfully downloaded object keys to bytes.
        """
        ...

    @abstractmethod
    async def delete_object(self, bucket_name: str, key: str):
        """
        Delete one object from a bucket.

        :param bucket_name: Source bucket name.
        :param key: Object key inside the bucket.
        """
        ...

    @abstractmethod
    async def delete_objects_batch(
        self, bucket_name: str, keys: list[dict[str, str]]
    ) -> None:
        """
        Delete multiple objects from a bucket.

        :param bucket_name: Source bucket name.
        :param keys: S3 delete-object descriptors, usually `{"Key": key}`.
        """
        ...

    @abstractmethod
    async def copy_object(self, bucket: str, key: str, new_key: str) -> None:
        """
        Copy an object to another key in the same bucket.

        :param bucket: Bucket name.
        :param key: Existing object key.
        :param new_key: Target object key.
        """
        ...
