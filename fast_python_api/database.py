from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)
from fast_python_api.settings import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# асинхронный движок
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Фабрика сессий
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# Синхронный движок (для работы в shell)
sync_engine = create_engine(
    settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql"),
    echo=True
)

# Фабрика синхронных сессий
SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False
)
