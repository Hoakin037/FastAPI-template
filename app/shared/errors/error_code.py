from enum import Enum

from .error_value import (
    AccessDeniedError,
    EntityNotFoundError,
    InvalidDataError,
    InvalidSortFieldError,
    NotUniqueError,
    UndefinedError,
    UnprocessableEntityError,
)


class SharedErrorCodes(Enum):
    UNDEFINED_ERROR = UndefinedError
    NOT_UNIQUE_ERROR = NotUniqueError
    ACCESS_DENIED_ERROR = AccessDeniedError
    ENTITY_NOT_FOUND_ERROR = EntityNotFoundError
    UNPROCESSABLE_ENTITY_ERROR = UnprocessableEntityError
    INVALID_SORT_FIELD_ERROR = InvalidSortFieldError
    INVALID_DATA_ERROR = InvalidDataError
