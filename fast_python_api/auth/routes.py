from typing import Annotated
from datetime import timedelta
from fast_python_api.settings import settings
from fast_python_api.chemas.token import Token
from sqlalchemy.ext.asyncio import AsyncSession
from fast_python_api.database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from fast_python_api.auth.token import create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from fast_python_api.auth.user_auth import authenticate_user


router = APIRouter(tags=["Auth"])


@router.post(
    "/token",
    summary="Get access token",
    description="Get access token. "
                "The returned token should be used in the Authorization "
                "header in the Bearer format.",
    response_model=Token,
    responses={
        200: {"description": "Token successfully created"},
        401: {"description": "Incorrect username or password"},
    }
)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> Token:
    """
    Get access token.
    This endpoint is used to obtain an access token. It takes in a username
    and password, and returns an access token if the credentials are valid.
    Args:
        form_data (OAuth2PasswordRequestForm): The username and password to
            authenticate with.
        session (AsyncSession): The database session to use.
    Returns:
        Token: The access token and its type.
    Raises:
        HTTPException: If the credentials are invalid, an HTTP 401 error
        is raised with a message "Incorrect username or password".
    Example:
        Request:
        POST /token
        Body: {"username": "user", "password": "pass"}
        Response:
        Status: 200 OK
        Body: {"access_token": "token", "token_type": "bearer"}
    """
    user = await authenticate_user(
        form_data.username, form_data.password, session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={
            "sub": user.login.username,
            "role": user.login.role,
            "id": str(user.login.uuid)
        },
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
