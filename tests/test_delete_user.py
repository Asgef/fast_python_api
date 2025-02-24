import pytest
from httpx import AsyncClient
from tests.test_token import generate_valid_token


headers_admin = {"Authorization": f"Bearer {generate_valid_token()}"}

headers_user = {"Authorization": f"Bearer {generate_valid_token(
    username='alice_smith',
    role='user',
    user_id='c647e0c3-d0fb-47fd-bbea-c61b3cd999dd'
)}"}



@pytest.mark.asyncio
async def test_delete_user_by_admin(
        test_client: AsyncClient, test_session
):
    user_uuid = 'c647e0c3-d0fb-47fd-bbea-c61b3cd999dd'
    response = await test_client.delete(
        f"/users/{user_uuid}/", headers=headers_admin
    )
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

    response = await test_client.get(
        f"/users/{user_uuid}", headers=headers_admin
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_delete_this_data(
        test_client: AsyncClient, test_session
):
    user_uuid = 'c647e0c3-d0fb-47fd-bbea-c61b3cd999dd'
    response = await test_client.delete(
        f"/users/{user_uuid}/", headers=headers_user
    )
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

    response = await test_client.get(
        f"/users/{user_uuid}", headers=headers_user
    )
    assert response.status_code == 404

    # response = await test_client.get(
    #     "/me", headers=headers_user
    # )
    # assert response.status_code == 401  # TODO Запретить доступ


@pytest.mark.asyncio
async def test_delete_other_user_data(
        test_client: AsyncClient, test_session
):
    user_uuid = '52cc33c2-7b60-4f8b-bc92-3aa92573c1dd'
    response = await test_client.delete(
        f"/users/{user_uuid}/", headers=headers_user
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_user_not_found(
        test_client: AsyncClient, test_session
):
    user_uuid = '52cc33c2-7b60-4f8b-bc92-3aa92573c1cc'
    response = await test_client.delete(
        f"/users/{user_uuid}/", headers=headers_admin
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_invalid_uuid(
        test_client: AsyncClient, test_session
):
    user_uuid = 'invalid_uuid'
    response = await test_client.delete(
        f"/users/{user_uuid}/", headers=headers_admin
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_without_access_token(
        test_client: AsyncClient, test_session
):
    user_uuid = 'c647e0c3-d0fb-47fd-bbea-c61b3cd999dd'
    response = await test_client.delete(
        f"/users/{user_uuid}/"
    )
    assert response.status_code == 401


# @pytest.mark.asyncio
# async def test_admin_cannot_delete_self(
#         test_client: AsyncClient, test_session
# ):
#     admin_uuid = 'admin_user_uuid'
#     response = await test_client.delete(
#         f"/users/{admin_uuid}/", headers=headers_admin
#     )
#     assert response.status_code == 403  # Нельзя отлынивать от работы
#
#
# @pytest.mark.asyncio
# async def test_user_cannot_delete_admin(
#         test_client: AsyncClient, test_session
# ):
#     admin_uuid = 'admin_user_uuid'
#     response = await test_client.delete(
#         f"/users/{admin_uuid}/", headers=headers_user
#     )
#     assert response.status_code == 403
