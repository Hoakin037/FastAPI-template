from uuid import UUID

from fastapi import Query
from pydantic import Field

from app.modules.users.consts import UsersSortBy
from app.shared.consts import SortDirection
from app.shared.schemas import CoreSchema


class UserFiltersQuery(CoreSchema):
    age_from: int = Query(None)
    age_to: int = Query(None)
    sid: UUID = Query(None)


class UserSortParamsQuery(CoreSchema):
    sort_by: UsersSortBy = Query(UsersSortBy.SID)
    sort_direction: SortDirection = Query(SortDirection.ASC)
