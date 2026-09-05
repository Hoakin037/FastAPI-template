from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.decorators import logg_function
from app.infrastructure.logger import setup_logging
from app.modules.users.filters.user import UserFilter
from app.modules.users.interfaces import IUserRepo
from app.modules.users.models import UserModel
from app.modules.users.schemas.user import UserCreate, UserUpdate
from app.shared.repositories import PostgresBaseRepo
from app.shared.schemas import CursorPaginationParams, PaginationParams
from app.shared.schemas.sort import SortParams


class UserRepo(PostgresBaseRepo[UserModel, UserCreate, UserUpdate], IUserRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session, model=UserModel, logger=setup_logging(__name__)
        )

    @logg_function(description="Get paginated users from db")
    async def get_paginated_users(
        self,
        pagination_params: PaginationParams,
        filters: UserFilter,
        sort_params: SortParams,
    ) -> tuple[Sequence[UserModel], int]:
        query = select(self.model)
        query = await self._apply_sorts(query, sort_params)
        query = await self._apply_filters(query, filters)

        return await self._apply_pagination(query, pagination_params)

    @logg_function(description="Get paginated users from db")
    async def get_cursor_paginated_users(
        self,
        pagination_params: CursorPaginationParams,
        filters: UserFilter,
        sort_params: SortParams,
    ) -> tuple[Sequence[UserModel], int]:
        query = select(self.model)
        query = await self._apply_sorts(query, sort_params)
        query = await self._apply_filters(query, filters)

        return await self._apply_cursor_pagination(query, pagination_params)
