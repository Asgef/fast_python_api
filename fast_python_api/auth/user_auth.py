from fastapi import HTTPException, Depends, status
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fast_python_api.settings import settings
from fast_python_api.chemas.token import TokenData
from fast_python_api.auth.token import oauth2_scheme
from fast_python_api.auth.hashing import verify_password
from fast_python_api.core.user_db import get_user_by_username
from sqlalchemy.ext.asyncio import AsyncSession
from fast_python_api.database import get_session
from fast_python_api.chemas.user_db import UserInDB
from fast_python_api.chemas.user_crud import UserPublic


async def authenticate_user(
        username: str, password: str, session: AsyncSession
) -> UserPublic | None:
    """
    Authenticate user by username and password.

    Args:
        username: The username to authenticate.
        password: The password to authenticate.
        session: The database session.

    Returns:
        The authenticated user if successful, otherwise None.
    """
    user = await get_user_by_username(username, session)

    if not user or not verify_password(password, user.login.password):
        return None

    return UserPublic(**user.to_dict())


async def verify_access_token(
        token: Annotated[str, Depends(oauth2_scheme)]
) -> TokenData:
    """
    Verify the provided access token and extract user information.

    Args:
        token: The JWT access token to verify.

    Returns:
        TokenData containing the user's username, role, and id.

    Raises:
        HTTPException: If the token is invalid or the credentials cannot be validated.
    """
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
        user_id: str = payload.get("id")
        if username is None:
            raise credentials_exception
        return TokenData(username=username, role=role, id=user_id)
    except InvalidTokenError:
        raise credentials_exception


async def get_current_user(
        token: Annotated[TokenData, Depends(verify_access_token)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserInDB | None:  # TODO: Разобраться, что делать с None
    """
    Get the current user by the provided access token.

    Args:
    - token: The access token to get the user from.
    - session: The database session to use.

    Returns:
    - The current user if found, otherwise None.
    """
    user = await get_user_by_username(username=token.username, session=session)
    return UserInDB(**user.to_dict())
