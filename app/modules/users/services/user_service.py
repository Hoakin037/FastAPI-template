from uuid import UUID

from app.infrastructure.decorators import logg_function
from app.infrastructure.logger import setup_logging
from app.modules.users.interfaces import IUserRepo
from app.modules.users.schemas.user import User, UserCreate, UserUpdate
from app.shared.errors.error_code import SharedErrorCodes
from app.shared.errors.exception import BackendException


class UserService:
    def __init__(self, user_repo: IUserRepo):
        self.user_repo = user_repo
        self._logger = setup_logging(__name__)

    @logg_function(description="Get user by sid")
    async def get_user(self, user_sid: UUID) -> User:
        user = await self.user_repo.get_by_sid(sid=user_sid)

        return User.model_validate(user)

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
        await self.user_repo.delete_by_sid(sid=user_sid)
