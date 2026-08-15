from aioboto3 import Session
from settings import S3Settings


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


def create_s3_client(settings: S3Settings) -> S3Client:
    return S3Client(
        endpoint_utl=settings.S3_ENDPOINT_URL,
        access_key_utl=settings.S3_ACCESS_KEY,
        secret_access_utl=settings.S3_SECRET_KEY,
        bucket=settings.S3_BUCKET,
    )
