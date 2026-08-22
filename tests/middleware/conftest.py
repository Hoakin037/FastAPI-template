import json
from collections.abc import Callable
from typing import Any

import pytest
from starlette.requests import Request
from starlette.responses import Response


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
