import os
import json
import pytest
import asyncio
import pytest_asyncio
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
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture()
def test_client():
    async def override_get_session():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)
