import os
import json
import pytest
import asyncio
from pathlib import Path
from fast_python_api.main import app
from fastapi.testclient import TestClient
from fast_python_api.settings import settings
from fast_python_api.models import Base, User
from fast_python_api.database import get_session
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)


test_engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False)


current_dir = os.getcwd()
fixtures = os.path.join(current_dir, "fixtures/users_dump.json")

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture()
async def test_session():
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    with open(fixtures, "r") as f:
        users_data = json.load(f)

    async with TestSessionLocal as session:
        for user_data in users_data:
            user = User(**user_data)
            session.add(user)
            await session.commit()

    yield # Выполнение тестов

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
def test_client(test_session):
    def override_get_session():
        return test_session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)

