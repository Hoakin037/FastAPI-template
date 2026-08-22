from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    REDIS_HOST: str = Field(default="localhost", alias="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, alias="REDIS_PORT")
    REDIS_DB: int = Field(default=0, alias="REDIS_DB")
    REDIS_PASSWORD: str | None = Field(default=None, alias="REDIS_PASSWORD")
    REDIS_DECODE_RESPONSES: bool = Field(default=True, alias="REDIS_DECODE_RESPONSES")
