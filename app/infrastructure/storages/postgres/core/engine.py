from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config import get_postgres_setting

database_url = get_postgres_setting().POSTGRES_DATABASE_URL
if database_url is None:
    raise Exception("Postgres database URL is not provided")

engine = create_async_engine(
    url=database_url.unicode_string(),
    pool_pre_ping=True,
    pool_size=get_postgres_setting().DB_POOL_SIZE,
    max_overflow=0,
)


def get_engine() -> AsyncEngine:
    return engine
