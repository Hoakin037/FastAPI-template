from typing import Any

from app.shared.schemas.core_schema import CoreSchema


class ExceptionModel(CoreSchema):
    http_status: int
    code: Any
    message: str

    @classmethod
    def get_error_response(cls) -> tuple[int, dict[str, Any]]:
        status_code = cls.model_fields["http_status"].default
        description = cls.model_fields["message"].default

        response_value: dict[str, Any] = {"model": cls, "description": description}

        return status_code, response_value
