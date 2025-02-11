from fastapi import APIRouter, Depends, Query
from typing import Annotated
from fast_python_api.auth.user import verify_access_token, get_users
from fast_python_api.chemas.user import UserPublic


router = APIRouter(prefix="/users", tags=["Users"])


@router.get('/', dependencies=[Depends(verify_access_token)])
async def get_users_list(
        items: Annotated[list[UserPublic], Depends(get_users)],
        skip: Annotated[int, Query()] = 0,
        limit: Annotated[int, Query()] = 100
):
    return items[skip: skip + limit]
