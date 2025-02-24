import pytest
from httpx import AsyncClient
from tests.test_token import generate_valid_token


headers={"Authorization": f"Bearer {generate_valid_token()}"}


@pytest.mark.asyncio
async def test_read_users(test_client: AsyncClient, test_session):
    response = await test_client.get("/users/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 18


@pytest.mark.asyncio
async def test_read_limit_users(test_client: AsyncClient, test_session):
    response = await test_client.get("/users?limit=5", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 5


@pytest.mark.asyncio
async def test_read_user(test_client: AsyncClient, test_session):
    user_uuid = "c647e0c3-d0fb-47fd-bbea-c61b3cd999dd"
    response = await test_client.get(f"/users/{user_uuid}/", headers=headers)
    assert response.status_code == 200
    assert response.json()["dob"] == "1992-03-15"
    assert response.json()["city"] == "New York"
    assert response.json()["email"] == "alice@example.com"
    assert response.json()["login"]["uuid"] == user_uuid
    assert response.json()["login"]["username"] == "alice_smith"
    assert response.json()["login"]["role"] == "user"
    assert response.json()["name"]["title"] == "Ms"
    assert response.json()["name"]["first_name"] == "Alice"
    assert response.json()["name"]["last_name"] == "Smith"


@pytest.mark.asyncio
async def test_read_user_not_found(test_client: AsyncClient, test_session):
    user_uuid = "c647e0c3-d0fb-47fd-bbea-c61b3cd999cc"
    response = await test_client.get(f"/users/{user_uuid}/", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_read_user_invalid_uuid(test_client: AsyncClient, test_session):
    user_uuid = "invalid_uuid"
    response = await test_client.get(f"/users/{user_uuid}/", headers=headers)
    assert response.status_code == 422
