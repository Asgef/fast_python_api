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
    dependencies=[Depends(verify_access_token)],
    responses={
        200: {
            "description": "Successful retrieval of users list",
            "content": {"application/json": {"example": [
                {
                    "name": {
                        "title": "string",
                        "first_name": "string",
                        "last_name": "string"
                    },
                    "login": {
                        "username": "string",
                        "role": "string",
                        "uuid": "string"
                    },
                    "dob": "string",
                    "city": "string",
                    "email": "string",
                    "created_at": "string"
                }
            ]}
            }
        },
        401: {"description": "Unauthorized, invalid or missing credentials"},
    }
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
    """
    Retrieve a list of users with pagination options.

    Args:
        session (AsyncSession): The database session.
        skip (int): Number of users to skip.
        limit (int): Maximum number of users to return.

    Returns:
        list[UserPublic]: List of public user data.

    Raises:
        HTTPException: 401 Unauthorized if credentials are invalid.
    """
    items = await get_users(session)
    return items[skip: skip + limit]


@router.get(
    '/{user_id}',
    dependencies=[Depends(verify_access_token)],
    summary="Retrieve a user by ID",
    description="Get a user by ID. Only accessible by logged in users.",
    responses={
        200: {"description": "Successful retrieval of user"},
        401: {"description": "Unauthorized, invalid or missing credentials"},
        404: {"description": "User not found"}
    }
)
async def get_user(
        user_id: Annotated[UUID, Path(description="The ID of the user")],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:
    """
    Retrieve a user by ID. Only accessible by logged in users.

    Args:
        user_id (UUID): The ID of the user.
        session (AsyncSession): The database session.

    Returns:
        UserPublic: The public representation of the user.

    Raises:
        HTTPException: 401 Unauthorized if credentials are invalid.
        HTTPException: 404 Not Found if the user does not exist.
    """
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
    description="Create a new user. Only accessible by admins.",
    responses={
        200: {"description": "User successfully created"},
        400: {"description": "Bad request, invalid data"},
        401: {"description": "Unauthorized, invalid or missing credentials"},
        403: {"description": "Forbidden, not enough permissions"}
    }
)
async def create_new_user(
        user_data: Annotated[UserCreate, UserCreate],
        current_user: Annotated[TokenData, Depends(verify_access_token)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:
    """
    Create a new user. Only accessible by admins.

    Args:
        user_data (UserCreate): Data for the new user.
        current_user (TokenData): The current authenticated user.
        session (AsyncSession): The database session.

    Returns:
        UserPublic: The public representation of the created user.

    Raises:
        HTTPException: 403 Forbidden if the user is not an admin.
    """
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
    description="Update a user. Only accessible by admins or the user themselves.", # noqa
    responses={
        200: {"description": "User successfully updated"},
        400: {"description": "Bad request, invalid data"},
        401: {"description": "Unauthorized, invalid or missing credentials"},
        403: {"description": "Forbidden, not enough permissions"},
        404: {"description": "User not found"}
    }
)
async def update_user_endpoint(
    user_id: UUID,
    update_data: UserUpdate,
    current_user: Annotated[TokenData, Depends(verify_access_token)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:
    """
    Update a user. Only accessible by admins or the user themselves.

    Args:
        user_id (UUID): ID of the user to update.
        update_data (UserUpdate): Data to update the user with.
        current_user (TokenData): The current authenticated user.
        session (AsyncSession): The database session.

    Returns:
        UserPublic: The public representation of the updated user.

    Raises:
        HTTPException: 403 Forbidden if the user does not have permission.
        HTTPException: 404 Not Found if the user does not exist.
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
    description="Delete a user. Only accessible by admins or the user themselves.", # noqa
    responses={
        200: {"description": "User successfully deleted"},
        401: {"description": "Unauthorized, invalid or missing credentials"},
        403: {"description": "Forbidden, not enough permissions"},
        404: {"description": "User not found"}
    }
)
async def delete_user_endpoint(
        user_id: UUID,
        current_user: Annotated[TokenData, Depends(verify_access_token)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPublic:
    """
    Delete a user. Only accessible by admins or the user themselves.

    Args:
        user_id (UUID): ID of the user to delete.
        current_user (TokenData): The current authenticated user.
        session (AsyncSession): The database session.

    Returns:
        UserPublic: The public representation of the deleted user.

    Raises:
        HTTPException: 403 Forbidden if the user does not have permission.
        HTTPException: 404 Not Found if the user does not exist.
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
            )

    await session.delete(user)
    await session.commit()
    return UserPublic(**user.to_dict())
