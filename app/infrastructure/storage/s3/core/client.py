from aioboto3 import Session
from aiobotocore.client import AioBaseClient

from app.config.settings import S3Settings


class S3Client:
    def __init__(self, settings: S3Settings):
        self.settings = settings

    def get_client(self) -> AioBaseClient:
        return Session().client(
            service_name="S3",
            endpoint_url=self.settings.S3_ENDPOINT_URL,
            aws_access_key_id=self.settings.S3_ACCESS_KEY,
            aws_secret_access_key=self.settings.S3_SECRET_KEY,
        )


async def get_s3_client(settings: S3Settings):
    return S3Client(settings=settings)
