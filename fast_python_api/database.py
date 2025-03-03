import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fast_python_api.settings import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)


# asynchronous engine
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Factory for sessions
async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_session() -> AsyncSession:
    """Yield an async session object.

    This is a factory for database sessions. It creates an async session
    object, which can be used as a context manager. The session object is
    an instance of the class `AsyncSession` from the `sqlalchemy.ext.asyncio`
    module.
    """
    async with async_session() as session:
        yield session


if "pytest" in sys.modules or __name__ == "__main__":
# Synchronous engine (for working in the shell)
    sync_engine = create_engine(
        settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql"),
        echo=True
    )

    # Factory for synchronous sessions
    SessionLocal = sessionmaker(
        bind=sync_engine,
        autocommit=False,
        autoflush=False
    )
