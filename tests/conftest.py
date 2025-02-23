import os
import json
import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import event
from datetime import date, datetime
from fastapi.testclient import TestClient
from fast_python_api.main import app
from fast_python_api.settings import settings
from fast_python_api.models import Base, User, Name, Login
from fast_python_api.database import get_session
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)


test_engine = create_async_engine(settings.TEST_DATABASE_URL, echo=True)


TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


FIXTURES_PATH = os.path.join(
    os.getcwd(), "tests", "fixtures", "users_dump.json"
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    async def init_db():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def load_fixtures():
        async with TestSessionLocal() as session:
            with open(FIXTURES_PATH, "r") as f:
                users_data = json.load(f)
            users = []
            for user_data in users_data:
                if "dob" in user_data:
                    user_data["dob"] = date.fromisoformat(user_data["dob"])
                if "created_at" in user_data:
                    user_data["created_at"] = datetime.fromisoformat(
                        user_data["created_at"]
                    )

                name_data = user_data.pop("name", None)
                login_data = user_data.pop("login", None)
                user = User(**user_data)
                if name_data:
                    user.name = Name(**name_data)
                if login_data:
                    user.login = Login(**login_data)
                users.append(user)
            session.add_all(users)
            await session.commit()

    async def drop_db():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(init_db())
    asyncio.run(load_fixtures())
    yield
    asyncio.run(drop_db())


@pytest_asyncio.fixture
async def test_session():
    connection = await test_engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection, expire_on_commit=False)
    yield session
    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture()
async def test_client(test_session):
    async def override_get_session():
        yield test_session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url="http://test",
            follow_redirects=True
    ) as client:
        yield client
