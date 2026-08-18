from typing import Annotated

from fastapi import APIRouter, Depends

from app.modules.users.schemas.user import User, UserCreate
from app.modules.users.services.deps import get_user_service
from app.modules.users.services.user_service import UserService

router = APIRouter()


@router.post("/users", response_model=User)
async def create_user(
    user: Annotated[UserCreate, UserCreate],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(user)
