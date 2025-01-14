from fastapi import FastAPI
from starlette.responses import JSONResponse
from aiohttp import ClientSession
from fast_python_api.settings import settings


app = FastAPI()


@app.get('/')
async def homepage():
    return JSONResponse({'Hello': 'World'})


@app.get('/test')
async def external_api_test():
    async with ClientSession() as session:
        async with session.get(
                settings.test_service_url, params=settings.param_test_api
        ) as response:
            return await response.json()
