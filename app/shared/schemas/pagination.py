from typing import Any, TypeVar

from pydantic import Field, computed_field

from app.shared.consts import SortDirection
from app.shared.utils import count_pages

from .core_schema import CoreSchema

ItemSchema = TypeVar("ItemSchema", bound=CoreSchema)
MAX_PAGE_LIMIT = 100


class PaginationParams(CoreSchema):
    limit: int = Field(default=20, ge=1, le=MAX_PAGE_LIMIT)
    offset: int = Field(default=0, ge=0)


class CursorPaginationParams(CoreSchema):
    limit: int = Field(default=20, ge=1, le=MAX_PAGE_LIMIT)
    cursor: Any
    cursor_direction: SortDirection


class PaginatedResult[ItemSchema](CoreSchema):
    items: list[ItemSchema]
    limit: int = Field(default=20, ge=1, le=MAX_PAGE_LIMIT)
    offset: int = Field(default=0, ge=0)
    total: int

    @computed_field
    def pages(self) -> int:
        return count_pages(
            total=self.total,
            limit=self.limit,
        )


class CursorPaginatedResult[ItemSchema](CoreSchema):
    items: list[ItemSchema]
    limit: int = Field(default=20, ge=1, le=MAX_PAGE_LIMIT)
    cursor: Any
    total: int
    cursor_direction: SortDirection

    @computed_field
    def pages(self) -> int:
        return count_pages(
            total=self.total,
            limit=self.limit,
        )
