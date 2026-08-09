from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config.settings import PostgresSettings


def create_engine(settings: PostgresSettings) -> AsyncEngine:
    database_url = settings.POSTGRES_DATABASE_URL
    if database_url is None:
        raise Exception("Postgres database URL is not provided")

    return create_async_engine(
        url=database_url.unicode_string(),
        pool_pre_ping=True,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=0,
    )
