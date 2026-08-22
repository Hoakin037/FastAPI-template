import pytest

from app.config.settings import S3Settings
from app.infrastructure.storage.s3 import create_s3_client


@pytest.fixture
async def s3_connection():
    settings = S3Settings()
    return create_s3_client(settings)
