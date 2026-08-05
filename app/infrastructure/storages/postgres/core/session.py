from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.requests import Request

from app.infrastructure.storages.postgres.core.engine import get_engine


def set_session_factory():
    return async_sessionmaker(
        bind=get_engine(),
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


async def get_db_session(request: Request) -> AsyncGenerator[Any, Any]:
    async with request.app.state.session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
