from aiohttp import ClientSession
from fast_python_api.settings import settings
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fast_python_api.database import get_session as get_db_session
from fast_python_api.services.utils import get_http_session
from fast_python_api.chemas.token import TokenData
from fast_python_api.chemas.params import RandomUserParams
from fast_python_api.auth.user_auth import verify_access_token
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
    Test external API, fetches random users.
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

) -> dict:
    """
    Import users from external API, only accessible by admins.
    """
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to import users"
        )
    users_data = await fetch_random_user(http_session, params)
    count_added_users = await create_user_bulk(users_data, db_session)
    return {"success": True, "imported_users": count_added_users}