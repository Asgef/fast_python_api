from fastapi import APIRouter, Depends, Query, Path, status, HTTPException
from typing import Annotated
from fast_python_api.auth.user_auth import verify_access_token
from fast_python_api.chemas.user_crud import UserPublic, UserCreate, UserUpdate
from fast_python_api.chemas.token import TokenData
from fast_python_api.core.user_db import get_users, get_user_by_id
from fast_python_api.core.user_crud import create_user, update_user
from fast_python_api.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


router = APIRouter(prefix="/users", tags=["Users"])


@router.get('/', dependencies=[Depends(verify_access_token)])
async def get_users_list(
        session: Annotated[AsyncSession, Depends(get_session)],
        skip: Annotated[int, Query()] = 0,
        limit: Annotated[int, Query()] = 100
) -> list[UserPublic]:
    items = await get_users(session)
    return items[skip: skip + limit]


@router.get('/{user_id}', dependencies=[Depends(verify_access_token)])
async def get_user(
        user_id: Annotated[UUID, Path()],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:
    user_db = await get_user_by_id(user_id, session)
    user = UserPublic(**user_db.to_dict())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post('/create')
async def create_new_user(
        user_data: Annotated[UserCreate, UserCreate],
        current_user: Annotated[TokenData, Depends(verify_access_token)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create users"
        )
    user = await create_user(user_data, session)
    return user


@router.put("/{user_id}", response_model=UserPublic)
async def update_user_endpoint(
    user_id: UUID,
    update_data: UserUpdate,
    current_user: Annotated[TokenData, Depends(verify_access_token)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    if current_user.role != 'admin' and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this user"
        )
    return await update_user(user_id, update_data, session)


@router.delete("/{user_id}")
async def delete_user_endpoint(
        user_id: UUID,
        current_user: Annotated[TokenData, Depends(verify_access_token)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:

    user = await get_user_by_id(user_id, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if current_user.role != 'admin' and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user"
        )

    await session.delete(user)
    await session.commit()
    return UserPublic(**user.to_dict())
