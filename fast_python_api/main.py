from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse
from typing import Annotated
from fast_python_api.services import extermal_api
from fast_python_api.auth import routes as auth_routes
from fast_python_api.auth.user import get_current_user
from fast_python_api.chemas.user import UserPublic
from fast_python_api import routes as users_router


app = FastAPI()


app.include_router(extermal_api.router)
app.include_router(auth_routes.router)
app.include_router(users_router.router)


@app.get('/')
async def homepage():
    return JSONResponse({'Hello': 'World'})


@app.get("/me", response_model=UserPublic)
async def read_users_me(
        current_user: Annotated[UserPublic, Depends(get_current_user)]
):
    return current_user
