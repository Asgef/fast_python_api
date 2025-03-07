from fast_python_api.settings import settings
from fast_python_api.database import get_session
from fast_python_api.models import User, Login, Name
from sqlalchemy.ext.asyncio import AsyncSession
from fast_python_api.chemas.user_db import UserInDB, LoginInDB, NameInDB
import asyncio
from fast_python_api.core.user_db import get_user_by_id


async def init_user(data: dict, session: AsyncSession) -> None:
    existing_user = await get_user_by_id(user_uuid=data['login']['uuid'], session=session)
    if existing_user:
        print(f'User {existing_user.login.username} already exists')
        return

    user_data = UserInDB(
        dob=data['dob'],
        city=data['city'],
        email=data['email'],
        id=str(data['login']['uuid']),
        login=LoginInDB(**data['login']),
        name=NameInDB(**data['name'])
    )

    user = User(**user_data.model_dump(exclude={"login", "name"}))
    login = Login(**user_data.login.model_dump())
    name = Name(**user_data.name.model_dump())


    try:
        session.add(user)
        session.add(login)
        session.add(name)
        await session.commit()
    except Exception as e:
        print(e)
        await session.rollback()

    print(f'User {user.login.username} added!!!')
    return


async def main():
    async for session in get_session():
        await init_user(data=admin, session=session)


if __name__ == '__main__':
    admin = {
        "id": "6c3b3609-6fae-4a71-a9fd-94eaabf12c9a",
        "dob": "1995-05-20",
        "city": "New York",
        "email": "testuser@example.com",
        "created_at": "2025-02-04 21:00:00+00:00",
        "name": {
            "user_id": "6c3b3609-6fae-4a71-a9fd-94eaabf12c9a",
            "title": "Mr",
            "first_name": "John",
            "last_name": "Doe"
        },
        "login": {
            "uuid": "6c3b3609-6fae-4a71-a9fd-94eaabf12c9a",
            "role": "admin",
            "username": "johndoe",
            "password": "$2b$12$5xCWw8DuLXfG1RY8sw9Zmuqse7Tdr4.5R3zUtxlF0Ct/6D2qne.5a"
        }
    }
    asyncio.run(main())
