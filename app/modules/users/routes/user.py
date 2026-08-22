from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path

from app.modules.users.schemas.user import User, UserCreate
from app.modules.users.services.deps import get_user_service
from app.modules.users.services.user_service import UserService

router = APIRouter()


@router.post("/users", response_model=User)
async def create_user(
    user: Annotated[UserCreate, Body()],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(user)


@router.get("/users/{user_sid}", response_model=User)
async def get_users(
    user_sid: Annotated[UUID, Path(alias="userSid")],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_user(user_sid)
