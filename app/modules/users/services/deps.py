from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.storage.postgres.deps import get_db_session

from ..repositories.deps import get_user_repo
from .user_service import UserService


async def get_user_service(session: Annotated[AsyncSession, Depends(get_db_session)]):
    user_repo = await get_user_repo(session)
    return UserService(user_repo=user_repo)
