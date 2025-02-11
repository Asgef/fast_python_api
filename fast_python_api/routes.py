from fastapi import APIRouter, Depends, Query, Path, status, HTTPException
from typing import Annotated
from fast_python_api.auth.user import (
    verify_access_token, get_users, get_user_by_id
)
from fast_python_api.chemas.user import UserPublic
from uuid import UUID


router = APIRouter(prefix="/users", tags=["Users"])


@router.get('/', dependencies=[Depends(verify_access_token)])
async def get_users_list(
        items: Annotated[list[UserPublic], Depends(get_users)],
        skip: Annotated[int, Query()] = 0,
        limit: Annotated[int, Query()] = 100
) -> list[UserPublic]:
    return items[skip: skip + limit]


@router.get('/{user_id}', dependencies=[Depends(verify_access_token)])
async def get_user(user_id: Annotated[UUID, Path()]) -> UserPublic:
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserPublic(**user.model_dump())
