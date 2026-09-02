from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, TypeVar

from pydantic import BaseModel
from app.shared.schemas import CursorPaginationParams, PaginationParams, SQLFilterBase
from app.shared.schemas.sort import SortParams
from sqlalchemy import ColumnElement, Select
from sqlalchemy.orm import Query
from sqlalchemy.sql.base import ExecutableOption

from app.shared.models import CoreModel

ModelType = TypeVar("ModelType", bound=CoreModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class IPostgresBaseRepo[ModelType, CreateSchema, UpdateSchema](ABC):
    @abstractmethod
    async def get_by_sid(
        self, sid: Any, options: Sequence[ExecutableOption] | None = None
    ) -> ModelType | None: ...

    @abstractmethod
    async def get_all(
        self,
        *where_clause: ColumnElement,
        options: Sequence[ExecutableOption] | None = None,
    ) -> Sequence[ModelType]: ...

    @abstractmethod
    async def create(
        self, obj: CreateSchema, with_commit: bool = True
    ) -> ModelType: ...

    @abstractmethod
    async def create_many(
        self, objs: Sequence[CreateSchema], with_commit: bool = True
    ) -> list[ModelType]: ...

    @abstractmethod
    async def update(
        self,
        db_obj: ModelType,
        obj: UpdateSchema | dict[str, Any],
        with_commit: bool = True,
    ) -> ModelType: ...

    @abstractmethod
    async def update_many(
        self,
        pairs: Sequence[tuple[ModelType, UpdateSchema | dict[str, Any]]],
        with_commit: bool = True,
    ) -> list[ModelType]: ...

    @abstractmethod
    async def delete(
        self, obj: ModelType | list[ModelType], with_commit: bool = True
    ) -> None: ...

    @abstractmethod
    async def delete_by_sid(
        self, sid: Any | list[Any], with_commit: bool = True
    ) -> None: ...

    @abstractmethod
    async def _apply_pagination(
        self, query: Select, pagination_params: PaginationParams
    ) -> tuple[Sequence[ModelType], int]: ...

    @abstractmethod
    async def _apply_cursor_pagination(
        self, query: Select, pagination_params: CursorPaginationParams
    ) -> tuple[Sequence[ModelType], int]: ...

    @abstractmethod
    async def _apply_sorts(
        self,
        query: Select,
        sort_params: SortParams,
    ) -> Select: ...

