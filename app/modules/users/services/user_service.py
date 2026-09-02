from uuid import UUID


from app.infrastructure.decorators import logg_function
from app.infrastructure.logger import setup_logging
from app.modules.users.filters.user import UserFilter
from app.modules.users.interfaces import IUserRepo
from app.modules.users.schemas.user import User, UserCreate, UserUpdate
from app.shared.errors.error_code import SharedErrorCodes
from app.shared.errors.exception import BackendException
from app.shared.schemas import (
    CursorPaginatedResult,
    CursorPaginationParams,
    PaginatedResult,
    PaginationParams,
SortParams
)


class UserService:
    def __init__(self, user_repo: IUserRepo):
        self.user_repo = user_repo
        self._logger = setup_logging(__name__)

    @logg_function(description="Get user by sid")
    async def get_user(self, user_sid: UUID) -> User:
        user = await self.user_repo.get_by_sid(sid=user_sid)
        if not user:
            raise BackendException(error=SharedErrorCodes.ENTITY_NOT_FOUND_ERROR)

        return User.model_validate(user)

    @logg_function(description="Get paginated users")
    async def get_paginated_users(
        self,
        pagination_params: PaginationParams,
        sort_params: SortParams,
        filters: UserFilter,
    ) -> PaginatedResult[User]:
        users, total = await self.user_repo.get_paginated_users(
            pagination_params, filters, sort_params
        )

        return PaginatedResult[User](
            items=[User.model_validate(user) for user in users],
            limit=pagination_params.limit,
            offset=pagination_params.offset,
            total=total,
        )

    @logg_function(description="Get cursor paginated users")
    async def get_cursor_paginated_users(
        self,
        pagination_params: CursorPaginationParams,
        sort_params: SortParams,
        filters: UserFilter,
    ) -> CursorPaginatedResult[User]:
        users, total = await self.user_repo.get_cursor_paginated_users(
            pagination_params, filters, sort_params
        )

        return CursorPaginatedResult[User](
            items=[User.model_validate(user) for user in users],
            limit=pagination_params.limit,
            cursor=pagination_params.cursor,
            total=total,
            cursor_direction=pagination_params.cursor_direction,
        )

    @logg_function(description="Create new user")
    async def create_user(self, user: UserCreate) -> User:
        new_user = await self.user_repo.create(user)

        return User.model_validate(new_user)

    @logg_function(description="Update user")
    async def update_user(self, user_sid: UUID, info_to_update: UserUpdate) -> User:
        current_user = await self.user_repo.get_by_sid(sid=user_sid)

        if not current_user:
            raise BackendException(error=SharedErrorCodes.ENTITY_NOT_FOUND_ERROR)

        updated_user = await self.user_repo.update(current_user, info_to_update)

        return User.model_validate(updated_user)

    @logg_function(description="Delete user")
    async def delete_user(self, user_sid: UUID) -> None:
        current_user = await self.user_repo.get_by_sid(sid=user_sid)

        if not current_user:
            raise BackendException(error=SharedErrorCodes.ENTITY_NOT_FOUND_ERROR)

        await self.user_repo.delete_by_sid(sid=user_sid)
