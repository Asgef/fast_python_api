from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Annotated
from fast_python_api.chemas.user_crud import UserPublic
from fast_python_api.models import User, Login
from fast_python_api.chemas.user_db import UserInDB
from fast_python_api.database import async_session
from pydantic import EmailStr
from sqlalchemy.sql import exists
import uuid


async def get_user_by_username(username: Annotated[str, Depends()]):
    async with async_session() as session:
        query = (
            select(User)
            .join(Login, User.id == Login.uuid)
            .options(joinedload(User.login), joinedload(User.name))
            .where(Login.username == username)
        )
        result = await session.execute(query)
        user_db = result.scalars().first()
    return UserInDB(**user_db.to_dict())


async def get_user_by_id(
        user_uuid: Annotated[uuid.UUID, Depends()]
) -> UserInDB | None:
    async with async_session() as session:
        query = (
            select(User)
            .join(Login, User.id == Login.uuid)
            .options(joinedload(User.login), joinedload(User.name))
            .where(User.id == str(user_uuid))
        )
        result = await session.execute(query)
        user_db = result.scalars().first()
    if not user_db:
        return None
    return UserInDB(**user_db.to_dict())


async def get_users():
    async with async_session() as session:
        query = (
            select(User)
            .join(Login, User.id == Login.uuid)
            .options(joinedload(User.login), joinedload(User.name))
        )
        result = await session.execute(query)
        users_db = result.scalars().all()
        return [UserPublic(**user.to_dict()) for user in users_db]


async def email_exists(email: EmailStr) -> bool:
    async with async_session() as session:
        query = select(exists().where(User.email == email))
        result = await session.execute(query)
    return result.scalar()


async def username_exists(username: str) -> bool:
    async with async_session() as session:
        query = select(exists().where(Login.username == username))
        result = await session.execute(query)
    return result.scalar()
