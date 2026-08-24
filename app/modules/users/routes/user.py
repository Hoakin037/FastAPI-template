from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.modules.users.schemas.user import User, UserCreate, UserUpdate
from app.modules.users.services.deps import get_user_service
from app.modules.users.services.user_service import UserService

router = APIRouter()


@router.get("/users/{userSid}", response_model=User)
async def get_users(
    user_sid: Annotated[UUID, Path(alias="userSid")],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_user(user_sid)


@router.post("/users", response_model=User)
async def create_user(
    user: Annotated[UserCreate, Body()],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(user)


@router.delete(
    "/users/{userSid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_sid: Annotated[UUID, Path(alias="userSid")],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    await user_service.delete_user(user_sid)


@router.put("/users/{userSid}", response_model=User)
async def update_user(
    user_sid: Annotated[UUID, Path(alias="userSid")],
    user: Annotated[UserUpdate, Body()],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.update_user(user_sid, user)
