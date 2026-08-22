import pytest

from app.config.settings import PostgresSettings
from app.infrastructure.storage.postgres import create_engine, create_session_factory


@pytest.fixture
async def database_connection():
    settings = PostgresSettings()
    engine = create_engine(settings)
    session_factory = create_session_factory(engine)

    async with session_factory() as session:
        yield session
