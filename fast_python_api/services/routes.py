from typing import Annotated
from aiohttp import ClientSession
from fast_python_api.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from fast_python_api.chemas.token import TokenData
from fast_python_api.chemas.user_db import UserInDB
from fast_python_api.chemas.user_crud import UserPublic
from fast_python_api.chemas.params import RandomUserParams
from fast_python_api.services.utils import get_http_session
from fastapi import APIRouter, Depends, HTTPException, status
from fast_python_api.auth.user_auth import verify_access_token
from fast_python_api.database import get_session as get_db_session
from fast_python_api.services.utils import (
    fetch_random_user, create_user_bulk
)


router = APIRouter(tags=["External API"])


@router.get(
    '/test',
    summary="Test external API",
    description="Test external API, fetches random users."
)
async def external_api_test(
        session: Annotated[ClientSession, Depends(get_http_session)],
        params: Annotated[RandomUserParams, Depends()]
) -> dict:
    """
    Fetches random users from an external API.

    This endpoint sends a request to the external API
    to retrieve random user data.
    It uses the provided session for making the HTTP
    request and the parameters
    defined in RandomUserParams for query parameters.

    Returns:
        dict: The JSON response from the external API
        containing random user data.

    Raises:
        HTTPException: If the external API is not accessible
        or returns an error.
    """
    q_params = params.model_dump(exclude_unset=True, exclude_none=True)
    response = await session.get(
        settings.test_service_url, params=q_params
    )  # TODO: Следует предусмотреть случай когда сервис не доступен
    return await response.json()


@router.post(
    '/import',
    summary="Import users from external API",
    description="Import users from external API, only accessible by admins."
)
async def import_users(
        params: Annotated[RandomUserParams, Depends()],
        current_user: Annotated[TokenData, Depends(verify_access_token)],
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        http_session: Annotated[ClientSession, Depends(get_http_session)]

) -> list[UserPublic]:
    """
    Import users from an external API.

    This endpoint allows admins to import users from an external API.
    It checks the role of the current user and raises a 403 Forbidden
    error if the user is not an admin. The function fetches user data
    and creates users in bulk in the database.

    Args:
        params (RandomUserParams): Parameters for fetching random users.
        current_user (TokenData): The currently authenticated user.
        db_session (AsyncSession): The database session
        for database operations.
        http_session (ClientSession): The HTTP session
        for making API requests.

    Returns:
        list[UserPublic]: A list of public user data
        after successful import.
    """
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to import users"
        )
    users_data: list[UserInDB] = await fetch_random_user(http_session, params)
    users: list[UserInDB] = await create_user_bulk(users_data, db_session)
    return [UserPublic(**user.model_dump()) for user in users]
