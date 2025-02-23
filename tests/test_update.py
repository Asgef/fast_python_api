import pytest
from httpx import AsyncClient
from tests.test_token import generate_valid_token


headers_admin = {"Authorization": f"Bearer {generate_valid_token()}"}

headers_user = {"Authorization": f"Bearer {generate_valid_token(
    username='alice_smith', role='user'
)}"}


@pytest.mark.asyncio
async def test_update_by_admin(
        test_client: AsyncClient, test_session
):
    user_uuid = 'c647e0c3-d0fb-47fd-bbea-c61b3cd999dd'
    user_data = {
        "name": {
            "last_name": "Johnson"
        },
        "login": {
            "username": "alice_jonson"
        },
        "city": "Chicago"
    }

    response = await test_client.put(
        f"/users/{user_uuid}/", json=user_data,
        headers=headers_admin
    )
    assert response.status_code == 200
    assert response.json()['city'] == user_data['city']
    assert response.json()['name']['last_name'] == user_data['name']['last_name']
    assert response.json()['login']['username'] == user_data['login']['username']


@pytest.mark.asyncio
async def test_user_update_this_data(
        test_client: AsyncClient, test_session
):
    user_uuid = 'c647e0c3-d0fb-47fd-bbea-c61b3cd999dd'
    user_data = {
        "name": {
            "last_name": "Johnson"
        },
        "login": {
            "username": "alice_jonson"
        },
        "city": "Chicago"
    }

    response = await test_client.put(
        f"/users/{user_uuid}/", json=user_data,
        headers=headers_admin
    )
    assert response.status_code == 200
    assert response.json()['city'] == user_data['city']
    assert response.json()['name']['last_name'] == user_data['name'][
        'last_name']
    assert response.json()['login']['username'] == user_data['login'][
        'username']


@pytest.mark.asyncio
async def test_update_other_user_data(
        test_client: AsyncClient, test_session
):
    user_uuid = '52cc33c2-7b60-4f8b-bc92-3aa92573c1dd'
    user_data = {
        "name": {
            "last_name": "Johnson"
        },
        "login": {
            "username": "alice_jonson"
        },
        "city": "Chicago"
    }
    response = await test_client.put(
        f"/users/{user_uuid}/", json=user_data,
        headers=headers_user
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_user_not_found(
        test_client: AsyncClient, test_session
):
    user_uuid = '52cc33c2-7b60-4f8b-bc92-3aa92573c1cc'
    user_data = {
        "city": "Chicago"
    }
    response = await test_client.put(
        f"/users/{user_uuid}/", json=user_data,
        headers=headers_admin
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user_invalid_uuid(
        test_client: AsyncClient, test_session
):
    user_uuid = 'invalid_uuid'
    user_data = {
        "city": "Chicago"
    }
    response = await test_client.put(
        f"/users/{user_uuid}/", json=user_data,
        headers=headers_admin
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_user_invalid_email(
        test_client: AsyncClient, test_session
):
    user_uuid = 'c647e0c3-d0fb-47fd-bbea-c61b3cd999dd'
    user_data = {
        "email": "invalid_email"
    }
    response = await test_client.put(
        f"/users/{user_uuid}/", json=user_data,
        headers=headers_admin
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_user_invalid_dob(
        test_client: AsyncClient, test_session
):
    user_uuid = 'c647e0c3-d0fb-47fd-bbea-c61b3cd999dd'
    user_data = {
        "dob": "invalid_dob"
    }
    response = await test_client.put(
        f"/users/{user_uuid}/", json=user_data,
        headers=headers_admin
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_without_access_token(
        test_client: AsyncClient, test_session
):
    user_uuid = 'c647e0c3-d0fb-47fd-bbea-c61b3cd999dd'
    user_data = {
        "city": "Chicago"
    }
    response = await test_client.put(
        f"/users/{user_uuid}/", json=user_data
    )
    assert response.status_code == 401
