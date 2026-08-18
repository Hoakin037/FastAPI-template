from app.modules.users.interfaces import IUserRepo
from app.modules.users.schemas.user import User, UserCreate


class UserService:
    def __init__(self, user_repo: IUserRepo):
        self.user_repo = user_repo

    async def create_user(self, user: UserCreate) -> User:
        new_user = await self.user_repo.create(user)
        return User.model_validate(new_user)
