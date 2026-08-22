from uuid import UUID

from app.modules.users.interfaces import IUserRepo
from app.modules.users.schemas.user import User, UserCreate, UserUpdate
from app.shared.errors.error_code import SharedErrorCodes
from app.shared.errors.exception import BackendException


class UserService:
    def __init__(self, user_repo: IUserRepo):
        self.user_repo = user_repo

    async def get_user(self, user_sid: UUID) -> User:
        user = await self.user_repo.get_by_sid(sid=user_sid)

        return User.model_validate(user)

    async def create_user(self, user: UserCreate) -> User:
        new_user = await self.user_repo.create(user)

        return User.model_validate(new_user)

    async def update_user(self, user_sid: UUID, info_to_update: UserUpdate) -> User:
        current_user = await self.user_repo.get_by_sid(sid=user_sid)

        if not current_user:
            raise BackendException(error=SharedErrorCodes.ENTITY_NOT_FOUND_ERROR)

        updated_user = await self.user_repo.update(current_user, info_to_update)

        return User.model_validate(updated_user)

    async def delete_user(
        self, current_user_sid: UUID, user_sid_to_delete: UUID
    ) -> None:
        if current_user_sid != user_sid_to_delete:
            raise BackendException(
                error=SharedErrorCodes.ACCESS_DENIED_ERROR,
            )

        await self.user_repo.delete_by_sid(sid=user_sid_to_delete)
