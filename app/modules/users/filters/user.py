from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter

from app.modules.users.models import UserModel
from app.shared.schemas import SQLFilterBase


class UserFilter(SQLFilterBase):
    age__gte: int | None = None
    age__lte: int | None = None
    sid: UUID | None = None

    class Constants(Filter.Constants):
        model = UserModel