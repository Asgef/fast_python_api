from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from fast_python_api.auth.user_auth import authenticate_user
from fast_python_api.auth.token import create_access_token
from fast_python_api.chemas.token import Token
from fast_python_api.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from fast_python_api.database import get_session


router = APIRouter(tags=["Auth"])


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> Token:
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
