from fastapi import HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fast_python_api.chemas.user import UserPublic
from fast_python_api.settings import settings
from fast_python_api.models import User, Login
from fast_python_api.chemas.user import UserInDB
from fast_python_api.chemas.token import TokenData
from fast_python_api.database import async_session
from fast_python_api.auth.token import oauth2_scheme
from fast_python_api.auth.hashing import verify_password
from uuid import UUID


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
        user_uuid: Annotated[UUID, Depends()]
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


async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)

    if not user or not verify_password(password, user.login.password):
        return False

    return user


async def verify_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception


async def get_current_user(
        token: Annotated[TokenData, Depends(verify_access_token)]
):
    user = await get_user_by_username(username=token.username)
    return user
