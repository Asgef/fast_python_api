from fastapi import HTTPException, Depends, status
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fast_python_api.settings import settings
from fast_python_api.chemas.token import TokenData
from fast_python_api.auth.token import oauth2_scheme
from fast_python_api.auth.hashing import verify_password
from fast_python_api.core.user_db import get_user_by_username


async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)

    if not user or not verify_password(password, user.login.password):
        return False

    return user


async def verify_access_token(
        token: Annotated[str, Depends(oauth2_scheme)]
) -> TokenData:
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
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        return TokenData(username=username, role=role)
    except InvalidTokenError:
        raise credentials_exception


async def get_current_user(
        token: Annotated[TokenData, Depends(verify_access_token)]
):
    user = await get_user_by_username(username=token.username)
    return user
