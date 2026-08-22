from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.storage.postgres.deps import get_db_session

from ..repositories.user_repo import UserRepo
from .user_service import UserService


async def get_user_service(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return UserService(user_repo=UserRepo(session=session))
