from asyncio import Semaphore

from s3 import S3Client


class S3BaseRepository:
    def __init__(self, client: S3Client):
        self.client = client
        self._semaphore = Semaphore(10)

    async def put_object(self, bucket_name: str, key: str, data: bytes) -> str: ...

    async def get_object(self, bucket_name: str, key: str) -> bytes: ...

    async def get_head_object(self, bucket: str, key: str) -> dict: ...

    async def get_objects_batch(
        self, bucket_name: str, keys: list[str]
    ) -> dict[str, bytes]: ...

    async def delete_object(self, bucket_name: str, key: str): ...

    async def delete_objects_batch(self, bucket_name: str, keys: list[str]) -> None: ...

    async def copy_object(self, bucket_name: str, key: str) -> None: ...
