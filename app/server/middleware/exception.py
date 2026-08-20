from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.infrastructure.logger import setup_logging
from app.shared.errors.error_value import UndefinedError, UnprocessableEntityError
from app.shared.errors.exception import BackendException

logger = setup_logging(__name__)


class BackendExceptionHandler:
    @staticmethod
    async def handle(_: Request, err: BackendException) -> JSONResponse:
        logger.exception("BackendException:")
        return err.response()


class ExceptionMiddleware:
    async def __call__(self, request: Request, call_next):
        try:
            return await call_next(request)

        except Exception as err:
            logger.exception(f"Unexpected error: {err}")
            undefined_exception = BackendException(error=UndefinedError())

            return undefined_exception.response()


class ValidationExceptionHandler:
    @staticmethod
    async def handle(
        _: Request,
        err: RequestValidationError,
    ) -> JSONResponse:
        logger.exception(f"ValidationException: {err}")
        unprocessable_entity_error = BackendException(
            error=UnprocessableEntityError(),
        )

        return unprocessable_entity_error.response()


class TypeValueExceptionHandler:
    @staticmethod
    async def handle(
        _: Request,
        err: TypeError | ValueError,
    ) -> JSONResponse:
        logger.exception(f"TypeValueException: {err}")
        unprocessable_entity_error = BackendException(
            error=UnprocessableEntityError(),
        )

        return unprocessable_entity_error.response()
