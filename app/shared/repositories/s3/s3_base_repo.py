import asyncio
from asyncio import Semaphore

from app.infrastructure.storage.s3 import S3Client


class S3BaseRepository:
    def __init__(self, client: S3Client):
        self.client = client
        self._semaphore = Semaphore(10)

    async def put_object(self, bucket_name: str, key: str, data: bytes) -> str:
        async with self.client.get_raw_client() as client:
            await client.put_object(Bucket=bucket_name, Key=key, Body=data)

        return key

    async def get_object(self, bucket_name: str, key: str) -> bytes:
        async with self.client.get_raw_client() as client:
            response = await client.get_object(Bucket=bucket_name, Key=key)
            data = await response["Body"].read()

            return data

    async def get_head_object(self, bucket: str, key: str) -> dict:
        async with self.client.get_raw_client() as client:
            response = await client.head_object(Bucket=bucket, Key=key)
            return response.get("Metadata", {})

    async def get_objects_batch(
        self, bucket_name: str, keys: list[str]
    ) -> dict[str, bytes]:
        if not keys:
            return {}

        result: dict[str, bytes] = {}

        async def _safe_download(key: str) -> None:
            try:
                async with self._semaphore:
                    data = await self.get_object(bucket_name, key)
                    result[key] = data

            except Exception:
                ...

        tasks = [_safe_download(key) for key in keys]
        await asyncio.gather(*tasks)

        return result

    async def delete_object(self, bucket_name: str, key: str):
        async with self.client.get_raw_client() as client:
            await client.delete_object(Bucket=bucket_name, Key=key)

    async def delete_objects_batch(
        self, bucket_name: str, keys: list[dict[str, str]]
    ) -> None:
        async with self.client.get_raw_client() as client:
            await client.delete_objects(
                Bucket=bucket_name, Delete={"Objects": keys, "Quiet": True}
            )

    async def copy_object(self, bucket: str, key: str, new_key: str) -> None:
        async with self.client.get_raw_client() as client:
            await client.copy_object(
                Bucket=bucket,
                CopySource={"Bucket": bucket, "Key": key},
                Key=new_key,
            )
