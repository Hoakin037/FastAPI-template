from abc import ABC
from collections.abc import Sequence

from app.modules.users.filters.user import UserFilter
from app.modules.users.models import UserModel
from app.modules.users.schemas.user import UserCreate, UserUpdate
from app.shared.interfaces.repositories import IPostgresBaseRepo
from app.shared.schemas import CursorPaginationParams, PaginationParams
from app.shared.schemas.sort import SortParams


class IUserRepo(IPostgresBaseRepo[UserModel, UserCreate, UserUpdate], ABC):
    async def get_paginated_users(
        self,
        pagination_params: PaginationParams,
        filters: UserFilter,
        sort_params: SortParams,
    ) -> tuple[Sequence[UserModel], int]: ...

    async def get_cursor_paginated_users(
        self,
        pagination_params: CursorPaginationParams,
        filters: UserFilter,
        sort_params: SortParams,
    ) -> tuple[Sequence[UserModel], int]: ...
