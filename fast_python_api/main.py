from fastapi import FastAPI
from starlette.responses import JSONResponse
from fast_python_api.services import extermal_api
from fast_python_api.auth import routes as auth_routes


app = FastAPI()


app.include_router(extermal_api.router)
app.include_router(auth_routes.router)


@app.get('/')
async def homepage():
    return JSONResponse({'Hello': 'World'})
