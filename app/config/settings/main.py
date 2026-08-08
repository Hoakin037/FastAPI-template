from pydantic_settings import BaseSettings
from settings import PostgresSettings, ProjectSettings, S3Settings
from settings.redis import RedisSettings


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings.model_validate({})
    redis: RedisSettings = RedisSettings.model_validate({})
    s3: S3Settings = S3Settings.model_validate({})
    project: ProjectSettings = ProjectSettings.model_validate({})
