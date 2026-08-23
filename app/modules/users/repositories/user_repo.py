from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.logger import setup_logging
from app.modules.users.interfaces import IUserRepo
from app.modules.users.models import UserModel
from app.modules.users.schemas.user import UserCreate, UserUpdate
from app.shared.repositories import PostgresBaseRepo


class UserRepo(PostgresBaseRepo[UserModel, UserCreate, UserUpdate], IUserRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session, model=UserModel, logger=setup_logging(__name__)
        )
