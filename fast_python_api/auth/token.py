import jwt
from typing import Any
from fast_python_api.settings import settings
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scheme_name="JSON Web Tokens",
    description="Enter your JWT token",
    auto_error=True,
)


def create_access_token(
        data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT token with the provided data.

    If ``expires_delta`` is not provided, the token will expire in 15 minutes.

    Args:
        data (dict[str, Any]): The data to encode in the token.
        expires_delta (timedelta | None): The time delta before
        the token expires.
            If not provided, the token will expire in 15 minutes.

    Returns:
        str: The JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt
