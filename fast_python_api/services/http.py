from typing import AsyncGenerator
from aiohttp import ClientSession


async def get_http_session() -> AsyncGenerator:
    async with ClientSession() as session:
        yield session
