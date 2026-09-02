from enum import StrEnum
from typing import TypeVar

from app.shared.consts import SortDirection

from .core_schema import CoreSchema

SortFields = TypeVar("SortFields", bound=StrEnum)


class SortParams(CoreSchema):
    sort_direction: SortDirection
    sort_field: SortFields
