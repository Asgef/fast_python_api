import os
import re
import json
import pytest
from httpx import AsyncClient
from aioresponses import aioresponses
from tests.test_token import generate_valid_token
from fast_python_api.settings import settings
from fast_python_api.logging_config import logger


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

    expected_url = f"{settings.test_service_url}?results=5"

    with aioresponses() as mocked:
        mocked.get(
            expected_url,
            payload=mocked_payload
        )

        response = await test_client.post("/import", headers=headers_admin)

    assert response.status_code == 200
    assert len(response.json()) == 5


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
    expected_url = f"{settings.test_service_url}?results=5"

    with aioresponses() as mocked:
        mocked.get(
            expected_url,
            payload=invalid_payload
        )
        response = await test_client.post(
            "/import", headers=headers_admin
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_import_users_server_error(
        test_client: AsyncClient, test_session
):
    expected_url = f"{settings.test_service_url}?results=5"

    with aioresponses() as mocked:
        mocked.get(
            expected_url,
            status=500
        )
        response = await test_client.post("/import", headers=headers_admin)

    assert response.status_code == 500
