from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, TypeVar

from pydantic import BaseModel
from sqlalchemy import ColumnElement, Select
from sqlalchemy.sql.base import ExecutableOption

from app.shared.models import CoreModel
from app.shared.schemas import CursorPaginationParams, PaginationParams
from app.shared.schemas.sort import SortParams

ModelType = TypeVar("ModelType", bound=CoreModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class IPostgresBaseRepo[ModelType, CreateSchema, UpdateSchema](ABC):
    """
    Base interface for asynchronous PostgreSQL repositories.

    Concrete repositories inherit this contract to expose common CRUD,
    pagination, and sorting behavior for SQLAlchemy models.
    """

    @abstractmethod
    async def get_by_sid(
        self, sid: Any, options: Sequence[ExecutableOption] | None = None
    ) -> ModelType | None:
        """
        Get one model instance by its public `sid`.

        :param sid: Public model identifier.
        :param options: Optional SQLAlchemy loader options.
        :return: Matching model instance or None when it does not exist.
        """
        ...

    @abstractmethod
    async def get_all(
        self,
        *where_clause: ColumnElement,
        options: Sequence[ExecutableOption] | None = None,
    ) -> Sequence[ModelType]:
        """
        Get all model instances matching optional SQLAlchemy conditions.

        :param where_clause: SQLAlchemy expressions applied to the query.
        :param options: Optional SQLAlchemy loader options.
        :return: Sequence of matching model instances.
        """
        ...

    @abstractmethod
    async def create(
        self, obj: CreateSchema, with_commit: bool = True
    ) -> ModelType:
        """
        Create and persist one model instance from a Pydantic schema.

        :param obj: Schema containing fields for the new model.
        :param with_commit: Whether to commit immediately or only flush.
        :return: Created model instance.
        """
        ...

    @abstractmethod
    async def create_many(
        self, objs: Sequence[CreateSchema], with_commit: bool = True
    ) -> list[ModelType]:
        """
        Create and persist multiple model instances.

        :param objs: Schemas containing fields for new models.
        :param with_commit: Whether to commit immediately or only flush.
        :return: Created model instances.
        """
        ...

    @abstractmethod
    async def update(
        self,
        db_obj: ModelType,
        obj: UpdateSchema | dict[str, Any],
        with_commit: bool = True,
    ) -> ModelType:
        """
        Update one existing model instance.

        :param db_obj: Persistent SQLAlchemy model instance to update.
        :param obj: Pydantic update schema or plain dict with changed fields.
        :param with_commit: Whether to commit immediately or only flush.
        :return: Updated model instance.
        """
        ...

    @abstractmethod
    async def update_many(
        self,
        pairs: Sequence[tuple[ModelType, UpdateSchema | dict[str, Any]]],
        with_commit: bool = True,
    ) -> list[ModelType]:
        """
        Update multiple existing model instances.

        :param pairs: Sequence of model and update-data pairs.
        :param with_commit: Whether to commit immediately or only flush.
        :return: Updated model instances.
        """
        ...

    @abstractmethod
    async def delete(
        self, obj: ModelType, with_commit: bool = True
    ) -> None:
        """
        Delete one model instance.

        :param obj: Persistent SQLAlchemy model instance to delete.
        :param with_commit: Whether to commit immediately or only flush.
        """
        ...

    @abstractmethod
    async def delete_by_sid(
        self, sid: Any | list[Any], with_commit: bool = True
    ) -> None:
        """
        Delete one or many model instances by public `sid`.

        :param sid: Public identifier or list of public identifiers.
        :param with_commit: Whether to commit immediately or only flush.
        """
        ...

    @abstractmethod
    async def _apply_pagination(
        self, query: Select, pagination_params: PaginationParams
    ) -> tuple[Sequence[ModelType], int]:
        """
        Apply offset pagination and calculate total count.

        :param query: SQLAlchemy select query before pagination.
        :param pagination_params: Limit and offset pagination settings.
        :return: Page items and total number of records.
        """
        ...

    @abstractmethod
    async def _apply_cursor_pagination(
        self, query: Select, pagination_params: CursorPaginationParams
    ) -> tuple[Sequence[ModelType], int]:
        """
        Apply cursor pagination and calculate total count.

        :param query: SQLAlchemy select query before pagination.
        :param pagination_params: Cursor, direction, and page size settings.
        :return: Page items and total number of records after cursor filtering.
        """
        ...

    @abstractmethod
    async def _apply_sorts(
        self,
        query: Select,
        sort_params: SortParams,
    ) -> Select:
        """
        Apply validated sorting to a SQLAlchemy query.

        :param query: SQLAlchemy select query before sorting.
        :param sort_params: Sort field and direction.
        :return: Query with ordering applied.
        """
        ...
