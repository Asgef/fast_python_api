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
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


async def get_formated_users(data: list[dict]) -> list[UserInDB]:
    """
    Converts a list of dicts from `randomuser.me` to `UserInDB` objects.

    Args:
        data (list[dict]): A list of dicts from `randomuser.me`.

    Returns:
        list[UserInDB]: A list of `UserInDB` objects.
    """

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
    return result  # TODO: Добавить проверку наличия ключей


async def create_user_bulk(
        users: list[UserInDB], session: AsyncSession
) -> list[UserInDB]:

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

        result = await session.execute(
            select(User)
            .options(joinedload(User.name), joinedload(User.login))
            .where(User.id.in_([u.id for u in users_data]))
        )
        users_data = result.scalars().all()

        return [UserInDB(**user.to_dict()) for user in users_data]

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
    """
    Gets a list of users from the external API and formats them
    into a list of UserInDB objects.

    Asynchronous function that gets a list of users from the external API
    and formats
    them into a list of UserInDB objects.
    Takes a ClientSession and a RandomUserParams object, then sends a GET
    request to the external API with the parameters specified in
    RandomUserParams, waits for the response and formats the result
    into a list of UserInDB objects.

    Args:
        session (ClientSession): ClientSession to perform the GET request.
        params (RandomUserParams): Parameters for the GET request.

    Returns:
        list[UserInDB]: List of UserInDB objects.

    Raises:
        HTTPException: If the external API returns an error status code,
            or if the response format is invalid.
    """
    q_params = params.model_dump(exclude_unset=True, exclude_none=True)
    async with session.get(
            settings.test_service_url, params=q_params
    ) as response:

        if response.status == 500:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="External API error"
            )

        data = await response.json()

        if "results" not in data or not isinstance(data["results"], list):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid response format from external API"
            )

        users_data = data['results']
        formated_users = await get_formated_users(users_data)
        return formated_users
