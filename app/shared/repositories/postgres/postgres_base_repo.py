from collections.abc import Sequence
from typing import Any, TypeVar

from pydantic import BaseModel
from sqlalchemy import ColumnElement, Result, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.shared.models import CoreModel

ModelType = TypeVar("ModelType", bound=CoreModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class PostgresBaseRepo[ModelType, CreateSchema, UpdateSchema]:
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model: type[ModelType] = model
        self.session: AsyncSession = session

    async def get_by_sid(
        self, sid: Any, options: Sequence[ExecutableOption] | None = None
    ) -> ModelType | None:
        query = select(self.model).where(self.model.sid == sid)

        if options:
            query = query.options(*options)

        result: Result = await self.session.execute(query)
        return result.scalars().first()

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

    async def create(self, obj: CreateSchema, with_commit: bool = True) -> ModelType:
        db_obj = self.model(**obj.model_dump())
        self.session.add(db_obj)

        if with_commit:
            await self.session.commit()
            await self.session.refresh(db_obj)
        else:
            await self.session.flush()

        return db_obj

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

    async def delete(self, obj: ModelType, with_commit: bool = True) -> None:
        await self.session.delete(obj)
        if with_commit:
            await self.session.commit()
        else:
            await self.session.flush()

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
