from collections.abc import AsyncGenerator
from typing import Any

from starlette.requests import Request


async def get_db_session(request: Request) -> AsyncGenerator[Any, Any]:
    async with request.app.state.session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
