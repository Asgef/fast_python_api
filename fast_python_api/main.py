from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse
from typing import Annotated
from fast_python_api.chemas.user_db import UserInDB
from fast_python_api.services import routes as external_api
from fast_python_api.auth import routes as auth_routes
from fast_python_api.auth.user_auth import get_current_user
from fast_python_api.chemas.user_crud import UserPublic
from fast_python_api.core import routes as users_router


app = FastAPI()


app.include_router(external_api.router)
app.include_router(auth_routes.router)
app.include_router(users_router.router)


@app.get('/')
async def homepage():
    return JSONResponse({'Hello': 'World'})


@app.get("/me")
async def read_users_me(
        current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserPublic:
    return UserPublic(**current_user.model_dump())
