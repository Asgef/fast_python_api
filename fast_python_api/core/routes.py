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


@router.get(
    '/',
    tags=["Users"],
    summary="Retrieve a list of users",
    description="Retrieve a list of users with pagination options. "
                "Use skip and limit query parameters to control the "
                "number of returned users.",
    dependencies=[Depends(verify_access_token)]
)
async def get_users_list(
        session: Annotated[AsyncSession, Depends(get_session)],
        skip: Annotated[
            int, Query(description="Number of users to skip", ge=0)
        ] = 0,
        limit: Annotated[
            int, Query(description="Maximum number of users to return", ge=1)
        ] = 5
) -> list[UserPublic]:
    """Retrieve a list of users with pagination options. """
    items = await get_users(session)
    return items[skip: skip + limit]


@router.get(
    '/{user_id}',
    dependencies=[Depends(verify_access_token)],
    summary="Retrieve a user by ID",
    description="Get a user by ID. Only accessible by logged in users."
)
async def get_user(
        user_id: Annotated[UUID, Path(description="The ID of the user")],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:
    """Retrieve a user by ID. Only accessible by logged in users."""
    user_db = await get_user_by_id(user_id, session)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user = UserPublic(**user_db.to_dict())
    return user


@router.post(
    '/create',
    summary="Create a new user",
    description="Create a new user. Only accessible by admins."
)
async def create_new_user(
        user_data: Annotated[UserCreate, UserCreate],
        current_user: Annotated[TokenData, Depends(verify_access_token)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:
    """Create a new user. Only accessible by admins."""
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create users"
        )
    user = await create_user(user_data, session)
    return user


@router.put(
    "/{user_id}",
    summary="Update a user",
    description="Update a user."
                "Only accessible by admins or the user themselves.",
)
async def update_user_endpoint(
    user_id: UUID,
    update_data: UserUpdate,
    current_user: Annotated[TokenData, Depends(verify_access_token)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:
    """
    Update a user. Only accessible by admins or the user themselves.
    """
    if current_user.role != 'admin':
        if current_user.id != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this user"
            )
    return await update_user(user_id, update_data, session)


@router.delete(
    "/{user_id}",
    summary="Delete a user",
    description="Delete a user. "
                "Only accessible by admins or the user themselves.",
)
async def delete_user_endpoint(
        user_id: UUID,
        current_user: Annotated[TokenData, Depends(verify_access_token)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:
    """
    Delete a user. Only accessible by admins or the user themselves.
    """
    user = await get_user_by_id(user_id, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if current_user.role != 'admin':
        if current_user.id != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this user"
            )  # TODO: Вынести проверку в отдельную функцию

    await session.delete(user)
    await session.commit()
    return UserPublic(**user.to_dict())
