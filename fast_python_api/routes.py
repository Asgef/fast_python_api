from fastapi import APIRouter, Depends
from typing import Annotated
from fast_python_api.auth.user import get_current_active_user
from fast_python_api.chemas.user import UserBase


router = APIRouter(prefix="/users", tags=["Users"])


@router.get('/')
async def get_users(
        items: Annotated[list[UserBase], Depends(get_current_active_user)],
        skip: int = 0,
        limit: int = 100
):
    return items[skip: skip + limit]
