from fastapi import HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fast_python_api.settings import settings
from fast_python_api.models import User, Login
from fast_python_api.chemas.user import UserInDB
from fast_python_api.chemas.token import TokenData
from fast_python_api.database import async_session
from fast_python_api.auth.token import oauth2_scheme
from fast_python_api.auth.hashing import verify_password


async def get_user(username: str):
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


async def authenticate_user(username: str, password: str):
    user = await get_user(username)

    if not user or not verify_password(password, user.login.password):
        return False

    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
