from collections.abc import Sequence
from contextlib import suppress
from logging import Logger
from typing import Any, TypeVar, cast

from pydantic import BaseModel
from sqlalchemy import (
    ColumnElement,
    Result,
    Select,
    delete,
    func,
    inspect,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import ColumnProperty, Query
from sqlalchemy.sql.base import ExecutableOption

from app.infrastructure.decorators import logg_function
from app.shared.consts import SortDirection
from app.shared.errors.error_code import SharedErrorCodes
from app.shared.errors.exception import BackendException
from app.shared.models import CoreModel
from app.shared.schemas import (
    CursorPaginationParams,
    PaginationParams,
    SortParams,
    SQLFilterBase,
)

ModelType = TypeVar("ModelType", bound=CoreModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class PostgresBaseRepo[ModelType, CreateSchema, UpdateSchema]:
    def __init__(self, model: type[ModelType], session: AsyncSession, logger: Logger):
        self.model: type[ModelType] = model
        self.session: AsyncSession = session
        self._logger = logger

    @logg_function(description="Get instance by sid")
    async def get_by_sid(
        self, sid: Any, options: Sequence[ExecutableOption] | None = None
    ) -> ModelType | None:
        query = select(self.model).where(self.model.sid == sid)

        if options:
            query = query.options(*options)

        result: Result = await self.session.execute(query)
        return result.scalars().first()

    @logg_function(description="Get instance")
    async def get_all(
        self,
        *where_clause: ColumnElement,
        options: Sequence[ExecutableOption] | None = None,
    ) -> Sequence[ModelType]:
        query = select(self.model)

        if where_clause:
            query = query.where(*where_clause)

        if options:
            query = query.options(*options)

        result: Result = await self.session.execute(query)
        return result.scalars().all()

    @logg_function(description="Create instance")
    async def create(self, obj: CreateSchema, with_commit: bool = True) -> ModelType:
        db_obj = self.model(**obj.model_dump())
        self.session.add(db_obj)

        if with_commit:
            await self.session.commit()
            await self.session.refresh(db_obj)
        else:
            await self.session.flush()

        return db_obj

    @logg_function(description="Create many instances")
    async def create_many(
        self, objs: Sequence[CreateSchema], with_commit: bool = True
    ) -> list[ModelType]:
        db_objs = [self.model(**u_object.model_dump()) for u_object in objs]
        self.session.add_all(db_objs)

        if with_commit:
            await self.session.commit()
        else:
            await self.session.flush()

        return db_objs

    @logg_function(description="Update instance")
    async def update(
        self,
        db_obj: ModelType,
        obj: UpdateSchema | dict[str, Any],
        with_commit: bool = True,
    ) -> ModelType:
        updated_data = (
            obj if isinstance(obj, dict) else obj.model_dump(exclude_unset=True)
        )

        for field, value in updated_data.items():
            setattr(db_obj, field, value)

        if with_commit:
            await self.session.commit()
            await self.session.refresh(db_obj)
        else:
            await self.session.flush()

        return db_obj

    @logg_function(description="Update many instances")
    async def update_many(
        self,
        pairs: Sequence[tuple[ModelType, UpdateSchema | dict[str, Any]]],
        with_commit: bool = True,
    ) -> list[ModelType]:
        updated_objs: list[ModelType] = []

        for db_obj, schema in pairs:
            updated_data = (
                schema
                if isinstance(schema, dict)
                else schema.model_dump(exclude_unset=True)
            )
            for field, value in updated_data.items():
                setattr(db_obj, field, value)
            updated_objs.append(db_obj)

        if with_commit:
            await self.session.commit()
        else:
            await self.session.flush()

        return updated_objs

    @logg_function(description="Delete instance")
    async def delete(self, obj: ModelType, with_commit: bool = True) -> None:
        await self.session.delete(obj)
        if with_commit:
            await self.session.commit()
        else:
            await self.session.flush()

    @logg_function(description="Delete instance by sid")
    async def delete_by_sid(
        self, sid: Any | list[Any], with_commit: bool = True
    ) -> None:
        if isinstance(sid, list):
            query = delete(self.model).where(self.model.sid.in_(sid))
            await self.session.execute(query)

        else:
            query = delete(self.model).where(self.model.sid == sid)
            await self.session.execute(query)

        if with_commit:
            await self.session.commit()
        else:
            await self.session.flush()

    async def get_total(self, query: Select):
        count_query = select(func.count()).select_from(query.subquery())
        total_row = await self.session.scalar(count_query)

        return cast("int", total_row)

    async def _apply_pagination(
        self, query: Select, pagination_params: PaginationParams
    ) -> tuple[Sequence[ModelType], int]:
        total = await self.get_total(query)

        paginated_query = query.limit(pagination_params.limit).offset(
            pagination_params.offset
        )
        items = await self.session.execute(paginated_query)
        items = items.scalars().all()

        return items, total

    async def _apply_cursor_pagination(
        self, query: Select, pagination_params: CursorPaginationParams
    ) -> tuple[Sequence[ModelType], int]:
        paginated_query = query.limit(pagination_params.limit).where(
            self.model.sid > pagination_params.cursor
            if pagination_params.cursor_direction == SortDirection.ASC
            else self.model.sid < pagination_params.cursor
        )
        total = await self.get_total(paginated_query)

        items = await self.session.execute(paginated_query)
        items = items.scalars().all()

        return items, total

    def _validate_sort_field(self, field_name: str) -> ColumnElement[Any]:
        mapper = inspect(self.model)

        mapped_attr = mapper.attrs.get(field_name)
        if isinstance(mapped_attr, ColumnProperty):
            return getattr(self.model, field_name)

        descriptor = mapper.all_orm_descriptors.get(field_name)
        if isinstance(descriptor, hybrid_property):
            field = getattr(self.model, field_name, None)

            try:
                expression = field.expression
            except (AttributeError, NotImplementedError) as exc:
                raise ValueError(
                    f"Cannot sort by hybrid property: {field_name}"  # noqa: EM102
                ) from exc

            return expression

        raise ValueError(f"Invalid sort field: {field_name}")  # noqa: EM102

    @staticmethod
    def _apply_sort_direction(
        sort_field: ColumnElement[Any], sort_direction: SortDirection
    ) -> Select:
        if sort_direction == SortDirection.DESC:
            return sort_field.desc()

        return sort_field.asc()

    async def _apply_sorts(
        self,
        query: Select,
        sort_params: SortParams,
    ) -> Select:
        if sort_params and sort_params.sort_field:
            try:
                sort_field = self._validate_sort_field(
                    str(sort_params.sort_field.value)
                )

                sort_field = self._apply_sort_direction(
                    sort_field, sort_params.sort_direction
                )

                with suppress(AttributeError, NotImplementedError):
                    sort_field = sort_field.nulls_last()

            except ValueError as exc:
                raise BackendException(
                    error=SharedErrorCodes.INVALID_SORT_FIELD_ERROR
                ) from exc

            else:
                return query.order_by(sort_field)

        return query

    @staticmethod
    async def _apply_filters(query: Select, filters: SQLFilterBase) -> Query | Select:
        return filters.filter(query)
