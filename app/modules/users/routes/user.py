from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Query
from starlette import status

from app.modules.users.schemas.user import User, UserCreate, UserUpdate
from app.modules.users.services.deps import get_user_service
from app.modules.users.services.user_service import UserService
from app.shared.errors.error_code import SharedErrorCodes
from app.shared.schemas import (
    CursorPaginatedResult,
    CursorPaginationParams,
    PaginatedResult,
    PaginationParams,
)
from app.shared.utils import generate_responses_from_errors

router = APIRouter()


@router.get(
    "/users/{userSid}",
    response_model=User,
    responses=generate_responses_from_errors(
        SharedErrorCodes.ENTITY_NOT_FOUND_ERROR,
        SharedErrorCodes.UNDEFINED_ERROR,
        SharedErrorCodes.UNPROCESSABLE_ENTITY_ERROR,
    ),
)
async def get_users(
    user_sid: Annotated[UUID, Path(alias="userSid")],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_user(user_sid)


@router.get(
    "/user/paginated",
    response_model=PaginatedResult[User],
    responses=generate_responses_from_errors(
        SharedErrorCodes.UNDEFINED_ERROR, SharedErrorCodes.UNPROCESSABLE_ENTITY_ERROR
    ),
)
async def get_paginated_users(
    pagination_params: Annotated[PaginationParams, Query()],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_paginated_users(pagination_params)


@router.get(
    "/user/cursor-paginated",
    response_model=CursorPaginatedResult[User],
    responses=generate_responses_from_errors(
        SharedErrorCodes.UNDEFINED_ERROR, SharedErrorCodes.UNPROCESSABLE_ENTITY_ERROR
    ),
)
async def get_cursor_paginated_users(
    pagination_params: Annotated[CursorPaginationParams, Query()],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_cursor_paginated_users(pagination_params)


@router.post(
    "/users",
    response_model=User,
    responses=generate_responses_from_errors(
        SharedErrorCodes.UNDEFINED_ERROR, SharedErrorCodes.UNPROCESSABLE_ENTITY_ERROR
    ),
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: Annotated[UserCreate, Body()],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(user)


@router.delete(
    "/users/{userSid}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_from_errors(
        SharedErrorCodes.UNDEFINED_ERROR, SharedErrorCodes.ENTITY_NOT_FOUND_ERROR
    ),
)
async def delete_user(
    user_sid: Annotated[UUID, Path(alias="userSid")],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    await user_service.delete_user(user_sid)


@router.patch(
    "/users/{userSid}",
    response_model=User,
    responses=generate_responses_from_errors(
        SharedErrorCodes.UNDEFINED_ERROR,
        SharedErrorCodes.ENTITY_NOT_FOUND_ERROR,
        SharedErrorCodes.UNPROCESSABLE_ENTITY_ERROR,
    ),
)
async def update_user(
    user_sid: Annotated[UUID, Path(alias="userSid")],
    user: Annotated[UserUpdate, Body()],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.update_user(user_sid, user)
