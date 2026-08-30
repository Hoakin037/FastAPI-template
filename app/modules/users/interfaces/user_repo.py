from abc import ABC
from collections.abc import Sequence

from app.modules.users.models import UserModel
from app.modules.users.schemas.user import UserCreate, UserUpdate
from app.shared.interfaces.repositories import IPostgresBaseRepo
from app.shared.schemas import CursorPaginationParams, PaginationParams


class IUserRepo(IPostgresBaseRepo[UserModel, UserCreate, UserUpdate], ABC):
    async def get_paginated_users(
        self, pagination_params: PaginationParams
    ) -> tuple[Sequence[UserModel], int]: ...

    async def get_cursor_paginated_users(
        self, pagination_params: CursorPaginationParams
    ) -> tuple[Sequence[UserModel], int]: ...
