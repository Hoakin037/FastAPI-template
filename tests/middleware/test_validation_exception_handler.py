from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from starlette.responses import JSONResponse

from app.server.middleware.exception import ValidationExceptionHandler


async def test_validation_handler_returns_422_for_request_validation_error(
    fake_request, response_json
) -> None:
    error = RequestValidationError([])

    response = await ValidationExceptionHandler.handle(fake_request, error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 422
    assert response_json(response) == {
        "http_status": 422,
        "code": "unprocessable_entity",
        "message": "Unprocessable Entity",
    }


async def test_validation_handler_hides_validation_details(
    fake_request, response_json
) -> None:
    error = RequestValidationError(
        [
            {
                "loc": ["body", "age"],
                "msg": "Input should be greater than 0",
                "type": "greater_than",
            }
        ]
    )

    response = await ValidationExceptionHandler.handle(fake_request, error)
    payload = response_json(response)

    assert response.status_code == 422
    assert "errors" not in payload
    assert "loc" not in response.body.decode()
    assert payload["code"] == "unprocessable_entity"


async def test_validation_handler_accepts_body_argument(
    fake_request, response_json
) -> None:
    error = RequestValidationError([], body={"age": -1})

    response = await ValidationExceptionHandler.handle(fake_request, error)

    assert response.status_code == 422
    assert response_json(response)["code"] == "unprocessable_entity"


async def test_validation_handler_supports_pydantic_validation_error(
    fake_request, response_json
) -> None:
    class DummyModel(BaseModel):
        age: int

    try:
        DummyModel(age="not-an-int")
    except ValidationError as err:
        response = await ValidationExceptionHandler.handle(fake_request, err)
    else:
        raise AssertionError("ValidationError was not raised")

    assert response.status_code == 422
    assert response_json(response)["code"] == "unprocessable_entity"


async def test_validation_handler_returns_json_content_type(fake_request) -> None:
    error = RequestValidationError([])

    response = await ValidationExceptionHandler.handle(fake_request, error)

    assert response.headers["content-type"].startswith("application/json")
