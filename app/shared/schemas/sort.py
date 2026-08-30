from enum import StrEnum

from app.shared.consts import SortDirection

from .core_schema import CoreSchema


class SortParams(CoreSchema):
    sort_direction: SortDirection
    sort_field: StrEnum
