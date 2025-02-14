from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fast_python_api.chemas.user_crud import UserPublic, UserCreate
from fast_python_api.models import User, Login, Name
from fast_python_api.database import async_session
from fast_python_api.auth.hashing import get_password_hash
from fast_python_api.core.user_db import email_exists, username_exists
import uuid


async def create_user(user_data: UserCreate) -> UserPublic:
    if await email_exists(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    if await username_exists(user_data.login.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    user_uuid = str(uuid.uuid4())

    user = User(
        id=user_uuid,
        **user_data.model_dump(exclude={"login", "name"}),

    )
    name = Name(
        user_id=user_uuid,
        **user_data.name.model_dump()
    )
    login = Login(
        uuid=user_uuid,
        username=user_data.login.username,
        password=get_password_hash(user_data.login.password)
    )

    async with async_session() as session:
        session.add_all([
            user, login, name
        ])
        await session.commit()
        result = await session.execute(
            select(User).options(
                joinedload(User.name),
                joinedload(User.login)
            ).where(User.id == user_uuid)
        )
        user = result.scalars().first()
    return UserPublic(**user.to_dict())
