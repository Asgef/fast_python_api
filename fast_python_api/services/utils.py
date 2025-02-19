from typing import Annotated
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
from fast_python_api.chemas.user_db import UserInDB, NameInDB, LoginInDB
from fast_python_api.settings import settings
from fast_python_api.services.http import get_http_session
from fastapi import Depends
from fast_python_api.models import User, Login, Name
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
from fast_python_api.chemas.params import RandomUserParams
from datetime import datetime


async def get_formated_users(data: list[dict]) -> list[UserInDB]:
    result = []
    for user in data:
        dob_str = user['dob']['date']
        dob_date = datetime.fromisoformat(dob_str[:10]).date()

        name_data = NameInDB(
            user_id=str(user['login']['uuid']),
            title=user['name']['title'],
            first_name=user['name']['first'],
            last_name=user['name']['last'],
        )
        login_data = LoginInDB(
            uuid=str(user['login']['uuid']),
            username=user['login']['username'],
            role='user',
            password=user['login']['sha256'],
        )
        user_data = UserInDB(
            id=str(user['login']['uuid']),
            dob=dob_date,
            city=user['location']['city'],
            email=user['email'],
            name=name_data,
            login=login_data
        )
        result.append(user_data)
    return result


async def create_user_bulk(
        users: list[UserInDB], session: AsyncSession
) -> int:
    users_data = []
    logins_data = []
    names_data = []

    for user in users:
        name = Name(**user.name.model_dump())
        login = Login(**user.login.model_dump())
        user = User(**user.model_dump(exclude={"name", "login"}))

        names_data.append(name)
        logins_data.append(login)
        users_data.append(user)

    try:
        session.add_all(users_data + logins_data + names_data)
        await session.commit()
        return len(users_data)

    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Integrity error: {str(e.orig)}"
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


async def fetch_random_user(
        session: Annotated[ClientSession, Depends(get_http_session)],
        params: RandomUserParams
) -> list[UserInDB]:
    q_params = params.model_dump(exclude_unset=True, exclude_none=True)
    async with session.get(
            settings.test_service_url, params=q_params
    ) as response:
        data = await response.json()
        users_data = data['results']
        formated_users = await get_formated_users(users_data)
        return formated_users
