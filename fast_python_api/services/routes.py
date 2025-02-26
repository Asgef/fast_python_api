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
    description="Test external API, fetches random users.",
    responses={
        200: {
            "description": "Ответ с данными о случайных пользователях",
            "content": {
                "application/json": {
                    "example": {
                        "results": [
                            {
                                "gender": "string",
                                "name": {
                                    "title": "string",
                                    "first": "string",
                                    "last": "string"
                                },
                                "location": {
                                    "street": {
                                        "number": "integer",
                                        "name": "string"
                                    },
                                    "city": "string",
                                    "state": "string",
                                    "country": "string",
                                    "postcode": "integer",
                                    "coordinates": {
                                        "latitude": "string",
                                        "longitude": "string"
                                    },
                                    "timezone": {
                                        "offset": "string",
                                        "description": "string"
                                    }
                                },
                                "email": "string",
                                "login": {
                                    "uuid": "string",
                                    "username": "string",
                                    "password": "string",
                                    "salt": "string",
                                    "md5": "string",
                                    "sha1": "string",
                                    "sha256": "string"
                                },
                                "dob": {
                                    "date": "string",
                                    "age": "integer"
                                },
                                "registered": {
                                    "date": "string",
                                    "age": "integer"
                                },
                                "phone": "string",
                                "cell": "string",
                                "id": {
                                    "name": "string",
                                    "value": "string"
                                },
                                "picture": {
                                    "large": "string",
                                    "medium": "string",
                                    "thumbnail": "string"
                                },
                                "nat": "string"
                            }
                        ],
                        "info": {
                            "seed": "string",
                            "results": "integer",
                            "page": "integer",
                            "version": "string"
                        }
                    }
                }
            }
        },
        500: {
            "description": "The external API is not accessible.",
        }
    }
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

    Args:
        session (ClientSession): The HTTP session
            for making API requests.
        params (RandomUserParams): Parameters for fetching random users.

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
    description="Import users from external API, only accessible by admins.",
    responses={
        200: {
            "description": "Users imported successfully.",
            "content": {
                "application/json": {
                    "example": [
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
                    ]
                }
            }
        },
        400: {
            "description": "The input parameters are invalid.",
        },
        401: {
            "description": "The user is not authenticated or "
                           "the token is invalid.",
        },
        403: {
            "description": "The user is not an admin.",
        }
    }
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
