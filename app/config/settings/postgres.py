from typing import Any

from pydantic import Field, PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    POSTGRES_HOST: str = Field(default="localhost", alias="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(default=5432, alias="POSTGRES_PORT")
    POSTGRES_USER: str = Field(default="postgres", alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="", alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="postgres", alias="POSTGRES_DB")

    POSTGRES_DATABASE_URL: PostgresDsn = PostgresDsn(url="postgresql://changme")

    @field_validator("POSTGRES_DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        options = {
            "scheme": "postgresql+asyncpg",
            "username": values.data.get("POSTGRES_USER"),
            "password": values.data.get("POSTGRES_PASSWORD"),
            "host": values.data.get("POSTGRES_HOST"),
            "port": values.data.get("POSTGRES_PORT"),
            "path": f"{values.data.get('POSTGRES_DB') or ''}",
        }
        return PostgresDsn.build(**options)

    DB_POOL_SIZE: int = Field(default=5, alias="DB_POOL_SIZE")
