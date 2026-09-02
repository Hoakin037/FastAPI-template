from typing import Literal

from starlette import status

from app.shared.errors.base_error_schema import ExceptionModel


class UndefinedError(ExceptionModel):
    http_status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: Literal["undefined_error"] = "undefined_error"
    message: str = "Undefined error"


class NotUniqueError(ExceptionModel):
    http_status: int = status.HTTP_409_CONFLICT
    code: Literal["not_unique"] = "not_unique"
    message: str = "Violation of data uniqueness"


class UnprocessableEntityError(ExceptionModel):
    http_status: int = status.HTTP_422_UNPROCESSABLE_CONTENT
    code: Literal["unprocessable_entity"] = "unprocessable_entity"
    message: str = "Unprocessable Entity"


class InvalidDataError(ExceptionModel):
    http_status: int = status.HTTP_400_BAD_REQUEST
    code: Literal["invalid_data"] = "invalid_data"
    message: str = "Invalid Data"


class InvalidSortFieldError(InvalidDataError):
    code: Literal["invalid_sort_field"] = "invalid_sort_field"
    message: str = "Invalid Sort Field"


class AccessDeniedError(ExceptionModel):
    http_status: int = status.HTTP_403_FORBIDDEN
    code: Literal["access_denied"] = "access_denied"
    message: str = "Access Denied"


class EntityNotFoundError(ExceptionModel):
    http_status: int = status.HTTP_404_NOT_FOUND
    code: Literal["entity_not_found"] = "entity_not_found"
    message: str = "Not Found"


class IncorrectSortFieldError(ExceptionModel):
    http_status: int = status.HTTP_400_BAD_REQUEST
    code: Literal["incorrect_sort_field"] = "incorrect_sort_field"
    message: str = "Incorrect Sort Field"
