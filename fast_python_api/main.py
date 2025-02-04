from fastapi import FastAPI
from starlette.responses import JSONResponse
from fast_python_api.services import extermal_api

app = FastAPI()


app.include_router(extermal_api.router)


@app.get('/')
async def homepage():
    return JSONResponse({'Hello': 'World'})
