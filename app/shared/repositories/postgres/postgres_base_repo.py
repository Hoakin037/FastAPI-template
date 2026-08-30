from collections.abc import Sequence
from contextlib import suppress
from logging import Logger
from typing import Any, TypeVar, cast

from app.shared.errors.error_code import SharedErrorCodes
from app.shared.errors.exception import BackendException
from pydantic import BaseModel
from app.shared.schemas.sort import SortParams
from sqlalchemy import Column, ColumnElement, Result, Select, delete, func, select
from sqlalchemy.ext.associationproxy import AssociationProxyInstance
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.base import SQLORMOperations
from sqlalchemy.sql.base import ExecutableOption

from app.infrastructure.decorators import logg_function
from app.shared.consts import SortDirection
from app.shared.models import CoreModel
from app.shared.schemas import CursorPaginationParams, PaginationParams

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

    async def _validate_sort_field(self, field_name: str) -> Column | SQLORMOperations:
        if not hasattr(self.model, field_name):
            raise ValueError(f"Invalid sort field: {field_name}")  # noqa: EM102

        field = getattr(self.model, field_name)
        field_descriptor = self.model.__dict__.get(field_name)
        mapper = class_mapper(self.model)

        if field_name in mapper.columns:
            return getattr(self.model, field_name)

        if isinstance(field, AssociationProxyInstance):
            remote_attr = field.remote_attr
            if remote_attr is None:
                raise ValueError(f"Cannot sort by proxy field: {field_name}")  # noqa: EM102
            return remote_attr

        if isinstance(field_descriptor, hybrid_property):
            try:
                return field.expression
            except (AttributeError, NotImplementedError):
                raise ValueError(f"Cannot sort by hybrid property: {field_name}")  # noqa: EM102, B904

        if field_name not in self.model.__table__.columns:
            raise ValueError(f"Not a column field: {field_name}")  # noqa: EM102

        return field

    async def _apply_sorts(
        self,
        query: Select,
        sort_params: SortParams,
    ) -> Select:
        if sort_params and sort_params.sort_direction:
            try:
                sort_field = await self._validate_sort_field(
                    str(sort_params.sort_field)
                )

                if sort_params.sort_direction == SortDirection.DESC:
                    sort_field = sort_field.desc()

                with suppress(AttributeError, NotImplementedError):
                    sort_field = sort_field.nulls_last()

            except ValueError as e:
                raise BackendException(
                    error=SharedErrorCodes.INCORRECT_SORT_FIELD
                ) from e

            else:
                return query.order_by(sort_field)

        return query
