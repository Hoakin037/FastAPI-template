from aioboto3 import Session
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from app.config.settings import S3Settings
from app.infrastructure.logger import setup_logging

logger = setup_logging(__name__)


class S3Client:
    def __init__(
        self,
        endpoint_utl: str,
        access_key_utl: str,
        secret_access_utl: str,
        bucket: str,
    ):
        self.endpoint_utl = endpoint_utl
        self.access_utl = access_key_utl
        self.secret_utl = secret_access_utl
        self.bucket = bucket
        self.Session = Session()

    def get_raw_client(self):
        return self.Session.client(
            service_name="s3",
            endpoint_url=self.endpoint_utl,
            aws_access_key_id=self.access_utl,
            aws_secret_access_key=self.secret_utl,
        )

    @staticmethod
    async def _create_bucket(client: BaseClient, bucket_name: str):
        try:
            await client.create_bucket(Bucket=bucket_name)

        except ClientError as err:
            error_code = err.response["Error"]["Code"]

            if error_code in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
                logger.warning(
                    f"Bucket '{bucket_name}' already exists, skipping creation"
                )

            else:
                raise

    async def init_buckets(self):
        async with self.get_raw_client() as client:
            await self._create_bucket(client, self.bucket)


def create_s3_client(settings: S3Settings) -> S3Client:
    return S3Client(
        endpoint_utl=settings.S3_ENDPOINT_URL,
        access_key_utl=settings.S3_ROOT_USER,
        secret_access_utl=settings.S3_ROOT_PASSWORD,
        bucket=settings.S3_BUCKET,
    )
