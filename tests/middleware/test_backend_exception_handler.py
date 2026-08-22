import logging

from starlette.responses import JSONResponse

from app.server.middleware.exception import BackendExceptionHandler
from app.shared.errors.error_code import SharedErrorCodes
from app.shared.errors.error_value import EntityNotFoundError, UndefinedError
from app.shared.errors.exception import BackendException

LOGGER_NAME = "app.server.middleware.exception"


async def test_backend_handler_returns_500_for_undefined_error(
    fake_request, response_json
) -> None:
    error = BackendException(error=SharedErrorCodes.UNDEFINED_ERROR)

    response = await BackendExceptionHandler.handle(fake_request, error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert response_json(response) == {
        "http_status": 500,
        "code": "undefined_error",
        "message": "Undefined error",
    }


async def test_backend_handler_returns_404_for_entity_not_found(
    fake_request, response_json
) -> None:
    error = BackendException(error=SharedErrorCodes.ENTITY_NOT_FOUND_ERROR)

    response = await BackendExceptionHandler.handle(fake_request, error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    assert response_json(response) == {
        "http_status": 404,
        "code": "entity_not_found",
        "message": "Not Found",
    }


async def test_backend_handler_accepts_exception_model_instance(
    fake_request, response_json
) -> None:
    error = BackendException(error=EntityNotFoundError())

    response = await BackendExceptionHandler.handle(fake_request, error)

    assert response.status_code == 404
    assert response_json(response)["code"] == "entity_not_found"


async def test_backend_handler_accepts_custom_error_instance(
    fake_request, response_json
) -> None:
    error = BackendException(error=UndefinedError())

    response = await BackendExceptionHandler.handle(fake_request, error)

    assert response.status_code == 500
    assert response_json(response)["code"] == "undefined_error"


async def test_backend_handler_returns_json_content_type(fake_request) -> None:
    error = BackendException(error=SharedErrorCodes.UNDEFINED_ERROR)

    response = await BackendExceptionHandler.handle(fake_request, error)

    assert response.headers["content-type"].startswith("application/json")


async def test_backend_handler_logs_backend_exception(fake_request, caplog) -> None:
    caplog.set_level(logging.ERROR, logger=LOGGER_NAME)

    error = BackendException(error=SharedErrorCodes.UNDEFINED_ERROR)
    await BackendExceptionHandler.handle(fake_request, error)

    assert "BackendException:" in caplog.text
