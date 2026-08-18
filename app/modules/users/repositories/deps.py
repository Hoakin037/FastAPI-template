from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.interfaces import IUserRepo
from app.modules.users.repositories.user_repo import UserRepo


async def get_user_repo(session: AsyncSession) -> IUserRepo:
    return UserRepo(
        session=session,
    )
