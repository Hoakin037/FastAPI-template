from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    HOST: str = Field(default="localhost", alias="HOST")
    PORT: int = Field(default=8000, alias="PORT")

    PROJECT_NAME: str = "FastAPI Template"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "FastAPI Template"

    LOG_LEVEL: str = Field(default="INFO", alias="LOG_LEVEL")

    CORS_ORIGINS: list[str] = Field(default=["*"], alias="CORS_ORIGINS")
