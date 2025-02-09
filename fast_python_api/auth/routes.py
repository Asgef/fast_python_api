from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from fast_python_api.auth.user import authenticate_user, get_current_user
from fast_python_api.auth.token import create_access_token
from fast_python_api.chemas.user import UserBase
from fast_python_api.chemas.token import Token
from fast_python_api.settings import settings


router = APIRouter(tags=["Auth"])


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
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
        data={"sub": user.login.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=UserBase)
async def read_users_me(
        current_user: Annotated[UserBase, Depends(get_current_user)]
):
    return current_user
