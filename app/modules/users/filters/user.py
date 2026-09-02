from uuid import UUID

from app.shared.schemas import SQLFilterBase


class UserFilter(SQLFilterBase):
    age__gte: int | None = None
    age__lte: int | None = None
    sid: UUID | None = None
