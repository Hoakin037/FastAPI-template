from pydantic_settings import BaseSettings

from .postgres import PostgresSettings
from .project import ProjectSettings
from .redis import RedisSettings
from .s3 import S3Settings


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings.model_validate({})
    redis: RedisSettings = RedisSettings.model_validate({})
    s3: S3Settings = S3Settings.model_validate({})
    project: ProjectSettings = ProjectSettings.model_validate({})
