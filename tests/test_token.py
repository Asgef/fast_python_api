import jwt
from fastapi import status
from fast_python_api.settings import settings
from datetime import datetime, timedelta, timezone
import pytest


@pytest.mark.asyncio
def generate_valid_token(
        username: str = "johndoe",
        role: str = "admin",
        user_id: str = "6c3b3609-6fae-4a71-a9fd-94eaabf12c9a"
) -> str:
    payload = {
        "sub": username,
        "role": role,
        "id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return token


@pytest.mark.asyncio
async def test_verify_valid_token(test_client):
    token = generate_valid_token()
    response = await test_client.get(
        '/me/', headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["login"]["username"] == "johndoe"
    assert data["login"]["role"] == "admin"


@pytest.mark.asyncio
async def test_verify_invalid_token(test_client):
    token = "invalid_token"
    response = await test_client.get(
        '/users/', headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


@pytest.mark.asyncio
async def test_verify_no_token(test_client):
    response = await test_client.get('/me/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}
