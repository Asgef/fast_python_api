import os
import re
import json
import pytest
from httpx import AsyncClient
from aioresponses import aioresponses
from tests.test_token import generate_valid_token


headers_admin = {"Authorization": f"Bearer {generate_valid_token()}"}
headers_user = {"Authorization": f"Bearer {generate_valid_token(
    username='alice_smith',
    role='user',
    user_id='c647e0c3-d0fb-47fd-bbea-c61b3cd999dd'
)}"}


FIXTURES_SERVICE_PATH = os.path.join(
    os.getcwd(), "tests", "fixtures", "service_response.json"
)


@pytest.mark.asyncio
async def test_import_users_success(test_client: AsyncClient, test_session):
    with open(FIXTURES_SERVICE_PATH, "r") as f:
        mocked_payload = json.load(f)

    with aioresponses() as mocked:
        mocked.get(re.compile(
            r'https://randomuser\.me/api.*'), payload=mocked_payload
        )
        response = await test_client.post("/import", headers=headers_admin)

    assert response.status_code == 200
    response_json = response.json()
    assert "imported_users" in response_json
    assert response_json["imported_users"] == len(
        mocked_payload.get("results", [])
    )


@pytest.mark.asyncio
async def test_import_users_forbidden_for_user(
        test_client: AsyncClient, test_session
):
    response = await test_client.post("/import", headers=headers_user)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_import_users_unauthorized(
        test_client: AsyncClient, test_session
):
    response = await test_client.post("/import")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_import_users_invalid_service_response(
        test_client: AsyncClient, test_session
):
    invalid_payload = {"unexpected": "data"}

    with aioresponses() as mocked:
        mocked.get(re.compile(
            r'https://randomuser\.me/api.*'), payload=invalid_payload
        )
        response = await test_client.post(
            "/import", headers=headers_admin
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_import_users_server_error(
        test_client: AsyncClient, test_session
):
    with aioresponses() as mocked:
        mocked.get(re.compile(r'https://randomuser\.me/api.*'), status=500)
        response = await test_client.post("/import", headers=headers_admin)

    assert response.status_code == 500
