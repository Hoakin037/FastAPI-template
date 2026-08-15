from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    S3_ENDPOINT_URL: str = Field(default="http://localhost:9015", alias="S3_HOST")
    S3_BUCKET: str = Field(default="bucket", alias="S3_BUCKET")
    S3_ROOT_USER: str = Field(default="key", alias="S3_ROOT_USER")
    S3_ROOT_PASSWORD: str = Field(default="secret", alias="S3_ROOT_PASSWORD")
