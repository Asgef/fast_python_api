from typing import AsyncGenerator
from aiohttp import ClientSession


async def get_http_session() -> AsyncGenerator[ClientSession, None]:
    """
    Get an aiohttp ClientSession that can be used to make HTTP requests.

    Yields:
        ClientSession: An aiohttp ClientSession.
    """
    async with ClientSession() as session:
        yield session
