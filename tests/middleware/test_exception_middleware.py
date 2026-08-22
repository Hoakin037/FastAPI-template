import json
from collections.abc import Callable
from typing import Any

import pytest
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response

from app.server.middleware.exception import ExceptionMiddleware
from app.shared.errors.error_code import SharedErrorCodes
from app.shared.errors.error_value import (
    EntityNotFoundError,
    UnprocessableEntityError,
)
from app.shared.errors.exception import BackendException


@pytest.fixture
def fake_request() -> Request:
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/",
        "raw_path": b"/",
        "query_string": b"",
        "root_path": "",
        "headers": [(b"host", b"testserver")],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    return Request(scope=scope)


@pytest.fixture
def response_json() -> Callable[[Response], dict[str, Any]]:
    def _response_json(response: Response) -> dict[str, Any]:
        return json.loads(response.body)

    return _response_json


async def test_middleware_returns_response_from_call_next(
    fake_request: Request,
) -> None:
    expected_response = PlainTextResponse("ok")

    async def call_next(request: Request) -> PlainTextResponse:  # noqa: ARG001
        return expected_response

    response = await ExceptionMiddleware()(fake_request, call_next)

    assert response is expected_response


async def test_middleware_passes_same_request_to_call_next(
    fake_request: Request,
) -> None:
    captured_requests: list[Request] = []

    async def call_next(request: Request) -> PlainTextResponse:
        captured_requests.append(request)
        return PlainTextResponse("ok")

    await ExceptionMiddleware()(fake_request, call_next)

    assert captured_requests == [fake_request]


async def test_middleware_preserves_entity_not_found_backend_exception(
    fake_request: Request,
    response_json: Callable[[Response], dict[str, Any]],
) -> None:
    async def call_next(request: Request) -> PlainTextResponse:  # noqa: ARG001
        raise BackendException(error=SharedErrorCodes.ENTITY_NOT_FOUND_ERROR)

    response = await ExceptionMiddleware()(fake_request, call_next)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    assert response_json(response) == {
        "http_status": 404,
        "code": "entity_not_found",
        "message": "Not Found",
    }


async def test_middleware_preserves_unprocessable_entity_backend_exception(
    fake_request: Request,
    response_json: Callable[[Response], dict[str, Any]],
) -> None:
    async def call_next(request: Request) -> PlainTextResponse:  # noqa: ARG001
        raise BackendException(error=SharedErrorCodes.UNPROCESSABLE_ENTITY_ERROR)

    response = await ExceptionMiddleware()(fake_request, call_next)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 422
    assert response_json(response) == {
        "http_status": 422,
        "code": "unprocessable_entity",
        "message": "Unprocessable Entity",
    }


async def test_middleware_preserves_backend_exception_instance(
    fake_request: Request,
    response_json: Callable[[Response], dict[str, Any]],
) -> None:
    async def call_next(request: Request) -> PlainTextResponse:  # noqa: ARG001
        raise BackendException(error=EntityNotFoundError())

    response = await ExceptionMiddleware()(fake_request, call_next)

    assert response.status_code == 404
    assert response_json(response) == {
        "http_status": 404,
        "code": "entity_not_found",
        "message": "Not Found",
    }


async def test_middleware_preserves_unprocessable_entity_error_instance(
    fake_request: Request,
    response_json: Callable[[Response], dict[str, Any]],
) -> None:
    async def call_next(request: Request) -> PlainTextResponse:  # noqa: ARG001
        raise BackendException(error=UnprocessableEntityError())

    response = await ExceptionMiddleware()(fake_request, call_next)

    assert response.status_code == 422
    assert response_json(response) == {
        "http_status": 422,
        "code": "unprocessable_entity",
        "message": "Unprocessable Entity",
    }


async def test_middleware_returns_500_for_unknown_exception(
    fake_request: Request,
    response_json: Callable[[Response], dict[str, Any]],
) -> None:
    async def call_next(request: Request) -> PlainTextResponse:  # noqa: ARG001
        raise RuntimeError("unexpected error")

    response = await ExceptionMiddleware()(fake_request, call_next)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert response_json(response) == {
        "http_status": 500,
        "code": "undefined_error",
        "message": "Undefined error",
    }


async def test_middleware_does_not_leak_unknown_exception_message(
    fake_request: Request,
    response_json: Callable[[Response], dict[str, Any]],
) -> None:
    secret_message = "secret-db-password-123"  # noqa: S105

    async def call_next(request: Request) -> PlainTextResponse:  # noqa: ARG001
        raise RuntimeError(secret_message)

    response = await ExceptionMiddleware()(fake_request, call_next)
    body = response.body.decode()

    assert secret_message not in body
    assert response_json(response)["message"] == "Undefined error"


async def test_middleware_error_response_has_json_content_type(
    fake_request: Request,
) -> None:
    async def call_next(request: Request) -> PlainTextResponse:  # noqa: ARG001
        raise RuntimeError("unexpected error")

    response = await ExceptionMiddleware()(fake_request, call_next)

    assert response.headers["content-type"].startswith("application/json")
