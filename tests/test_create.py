import pytest
from httpx import AsyncClient
from tests.test_token import generate_valid_token


headers={"Authorization": f"Bearer {generate_valid_token()}"}


@pytest.mark.asyncio
async def test_create_user_success(test_client: AsyncClient, test_session):
    user_data = {
        "name": {
            "title": "Mr",
            "first_name": "Johni",
            "last_name": "Doi"
        },
        "login": {
            "username": "johndoi",
            "password": "secret",
            "role": "user"
        },
        "dob": "1990-01-01",
        "city": "New York",
        "email": "johndoi@example.com"
    }

    response = await test_client.post(
        "/users/create/", json=user_data, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["login"]["username"] == user_data["login"]["username"]


@pytest.mark.asyncio
async def test_create_user_duplicate_email(test_client: AsyncClient, test_session):
    user_data = {
        "name": {
            "title": "Mr",
            "first_name": "Jane",
            "last_name": "Doe"
        },
        "login": {
            "username": "janedoe",
            "password": "secret",
            "role": "user"
        },
        "dob": "1992-03-15",
        "city": "Los Angeles",
        "email": "testuser@example.com"
    }

    response = await test_client.post("/users/create/", json=user_data, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists"


@pytest.mark.asyncio
async def test_create_user_duplicate_username(test_client: AsyncClient, test_session):
    user_data = {
        "name": {
            "title": "Ms",
            "first_name": "Alice",
            "last_name": "Smith"
        },
        "login": {
            "username": "johndoe",
            "password": "secret",
            "role": "user"
        },
        "dob": "1995-06-10",
        "city": "Chicago",
        "email": "alice@example.com"
    }

    response = await test_client.post(
        "/users/create/", json=user_data, headers=headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists"


@pytest.mark.asyncio
async def test_create_user_invalid_email(test_client: AsyncClient):
    user_data = {
        "name": {
            "title": "Mr",
            "first_name": "Invalid",
            "last_name": "User"
        },
        "login": {
            "username": "invaliduser",
            "password": "secret",
            "role": "user"
        },
        "dob": "2000-01-01",
        "city": "Seattle",
        "email": "invalid-email"
    }

    response = await test_client.post(
        "/users/create/", json=user_data, headers=headers
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_missing_fields(test_client: AsyncClient):
    user_data = {
        "name": {"first_name": "No", "last_name": "Fields"},
        "login": {"username": "nofields", "password": "secret"},
        "dob": "2000-01-01"
    }

    response = await test_client.post(
        "/users/create/", json=user_data, headers=headers
    )
    assert response.status_code == 422
