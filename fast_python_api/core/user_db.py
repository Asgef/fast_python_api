from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Annotated
from fast_python_api.chemas.user_crud import UserPublic
from fast_python_api.models import User, Login
from fast_python_api.chemas.user_db import UserInDB
from fast_python_api.database import async_session, get_session
from pydantic import EmailStr
from sqlalchemy.sql import exists
from sqlalchemy.ext.asyncio import AsyncSession
import uuid


async def get_user_by_username(
        username: Annotated[str, Depends()],
        session: AsyncSession
) -> User | None:
    query = (
        select(User)
        .join(Login, User.id == Login.uuid)
        .options(joinedload(User.login), joinedload(User.name))
        .where(Login.username == username)
    )
    result = await session.execute(query)
    return result.scalars().first()


async def get_user_by_id(
        user_uuid: Annotated[uuid.UUID, Depends()],
        session: AsyncSession
) -> User | None:
    query = (
        select(User)
        .join(Login, User.id == Login.uuid)
        .options(joinedload(User.login), joinedload(User.name))
        .where(User.id == str(user_uuid))
    )
    result = await session.execute(query)
    return result.scalars().first()


async def get_users(session: AsyncSession) -> list[UserPublic]:
    query = (
        select(User)
        .join(Login, User.id == Login.uuid)
        .options(joinedload(User.login), joinedload(User.name))
    )
    result = await session.execute(query)
    users_db = result.scalars().all()
    return [UserPublic(**user.to_dict()) for user in users_db]


async def email_exists(email: EmailStr, session: AsyncSession) -> bool:
    query = select(exists().where(User.email == email))
    result = await session.execute(query)
    return result.scalar()


async def username_exists(username: str, session: AsyncSession) -> bool:
    query = select(exists().where(Login.username == username))
    result = await session.execute(query)
    return result.scalar()
