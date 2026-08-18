import uuid
from uuid import UUID

from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.storage.postgres import PostgresSchemas
from app.infrastructure.storage.postgres.utils.table_args import table_args
from app.shared.models import CoreModel


class UserModel(CoreModel):
    __table_args__ = table_args(schema=PostgresSchemas.USERS)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(length=72), nullable=False)
    surname: Mapped[str] = mapped_column(String(length=72), nullable=False)
    age: Mapped[int] = mapped_column(
        Integer, CheckConstraint("age BETWEEN 0 AND 100"), nullable=False
    )
