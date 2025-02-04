from aiohttp import ClientSession
from fast_python_api.settings import settings
from fastapi import APIRouter


router = APIRouter(tags=["External API"])


@router.get('/test')
async def external_api_test():
    async with ClientSession() as session:
        async with session.get(
                settings.test_service_url, params=settings.param_test_api
        ) as response:
            return await response.json()
