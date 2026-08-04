from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends

from app.infrastructure.storages.s3.core.client import S3Client, get_s3_client


@asynccontextmanager
async def get_session(s3_client: Annotated[S3Client, Depends(get_s3_client)]):
    async with await s3_client.get_client() as client:
        yield client
