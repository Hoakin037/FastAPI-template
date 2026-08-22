from collections.abc import AsyncGenerator
from typing import Any

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from app.infrastructure.logger import setup_logging
from app.shared.errors.error_code import SharedErrorCodes
from app.shared.errors.exception import BackendException

logger = setup_logging(__name__)


async def get_db_session(request: Request) -> AsyncGenerator[Any, Any]:
    async with request.app.state.session_factory() as session:
        try:
            yield session

        except (RequestValidationError, BackendException):
            await session.rollback()

            raise

        except Exception as err:
            await session.rollback()
            logger.exception(f"Unexpected error: {err}")  # noqa: TRY401

            raise BackendException(error=SharedErrorCodes.UNDEFINED_ERROR) from err
