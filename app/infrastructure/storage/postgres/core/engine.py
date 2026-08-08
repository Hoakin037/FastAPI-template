from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config import get_postgres_setting
from app.config.settings import PostgresSettings

database_url = get_postgres_setting().POSTGRES_DATABASE_URL
if database_url is None:
    raise Exception("Postgres database URL is not provided")


def create_engine(settings: PostgresSettings) -> AsyncEngine:
    return create_async_engine(
        url=settings.POSTGRES_DATABASE_URL.unicode_string(),
        pool_pre_ping=True,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=0,
    )
