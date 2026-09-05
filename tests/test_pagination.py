import pytest
from pydantic import ValidationError

from app.shared.consts import SortDirection
from app.shared.schemas.pagination import (
    MAX_PAGE_LIMIT,
    CursorPaginatedResult,
    CursorPaginationParams,
    PaginatedResult,
    PaginationParams,
)
from app.shared.utils import count_pages


def test_count_pages_rejects_zero_limit():
    with pytest.raises(ValueError):
        count_pages(total=10, limit=0)


def test_pagination_params_reject_invalid_limit_and_offset():
    with pytest.raises(ValidationError):
        PaginationParams(limit=0)

    with pytest.raises(ValidationError):
        PaginationParams(limit=MAX_PAGE_LIMIT + 1)

    with pytest.raises(ValidationError):
        PaginationParams(offset=-1)


def test_cursor_pagination_params_reject_invalid_limit():
    with pytest.raises(ValidationError):
        CursorPaginationParams(
            limit=0,
            cursor="cursor",
            cursor_direction=SortDirection.ASC,
        )


def test_paginated_results_reject_invalid_limit_and_offset():
    with pytest.raises(ValidationError):
        PaginatedResult(items=[], total=0, limit=0)

    with pytest.raises(ValidationError):
        PaginatedResult(items=[], total=0, offset=-1)


def test_cursor_paginated_result_rejects_invalid_limit():
    with pytest.raises(ValidationError):
        CursorPaginatedResult(
            items=[],
            total=0,
            limit=0,
            cursor="cursor",
            cursor_direction=SortDirection.ASC,
        )
