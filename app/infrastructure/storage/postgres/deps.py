from collections.abc import AsyncGenerator
from typing import Any

from starlette.requests import Request

from app.shared.errors.exception import BackendException


async def get_db_session(request: Request) -> AsyncGenerator[Any, Any]:
    async with request.app.state.session_factory() as session:
        try:
            yield session

        except Exception as err:
            await session.rollback()
            raise BackendException from err
