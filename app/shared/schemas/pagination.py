from typing import Any, TypeVar

from pydantic import computed_field

from app.shared.consts import SortDirection
from app.shared.utils import count_pages

from .core_schema import CoreSchema

ItemSchema = TypeVar("ItemSchema", bound=CoreSchema)


class PaginationParams(CoreSchema):
    limit: int = 20
    offset: int = 0


class CursorPaginationParams(CoreSchema):
    limit: int = 20
    cursor: Any
    cursor_direction: SortDirection


class PaginatedResult[ItemSchema](CoreSchema):
    items: list[ItemSchema]
    limit: int = 20
    offset: int = 0
    total: int

    @computed_field
    def pages(self) -> int:
        return count_pages(
            total=self.total,
            limit=self.limit,
        )


class CursorPaginatedResult[ItemSchema](CoreSchema):
    items: list[ItemSchema]
    limit: int = 20
    cursor: Any
    total: int
    cursor_direction: SortDirection

    @computed_field
    def pages(self) -> int:
        return count_pages(
            total=self.total,
            limit=self.limit,
        )
