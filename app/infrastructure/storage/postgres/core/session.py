from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from starlette.requests import Request


def create_session_factory(engine: AsyncEngine):
    return async_sessionmaker(
        bind=engine,
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
