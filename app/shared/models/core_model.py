from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class CoreModel(DeclarativeBase):
    sid: Any

    # sid: int

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC).replace(microsecond=0),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC).replace(microsecond=0),
        onupdate=lambda: datetime.now(UTC).replace(microsecond=0),
    )

    @declared_attr  # pyright: ignore[reportArgumentType]
    def __tablename__(cls) -> str:
        name = cls.__name__.replace("Model", "")
        res = [name[0].lower()]
        for c in name[1:]:
            if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                res.append("_")
                res.append(c.lower())
            else:
                res.append(c)
        cls.__name__ = "".join(res)
        return cls.__name__
