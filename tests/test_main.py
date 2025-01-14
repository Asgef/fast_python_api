import pytest
from fastapi.testclient import TestClient
from aiohttp import ClientSession
from aioresponses import aioresponses
from fast_python_api.main import app
from fast_python_api.settings import settings


client = TestClient(app)

PARAMS_TEST_API = {'results': 5, 'inc': 'name,email'}

def test_homepage():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'Hello': 'World'}


@pytest.mark.asyncio
async def test_external_api_test():
    pyload = {
        'results': [
            {'name': {'title': 'Mrs', 'first': 'Iina', 'last': 'Kantola'},
              'email': 'iina.kantola@example.com'},
             {'name': {'title': 'Miss', 'first': 'Iolanda', 'last': 'Silveira'},
              'email': 'iolanda.silveira@example.com'},
             {'name': {'title': 'Mrs', 'first': 'Elma', 'last': 'Ederveen'},
              'email': 'elma.ederveen@example.com'},
             {'name': {'title': 'Mr', 'first': 'Anastácio', 'last': 'da Costa'},
              'email': 'anastacio.dacosta@example.com'},
             {'name': {'title': 'Mrs', 'first': 'Marine', 'last': 'Lefebvre'},
              'email': 'marine.lefebvre@example.com'}
        ],
         'info': {'seed': '25a8adac11c81aa4',
                  'results': 5,
                  'page': 1,
                  'version': '1.4'}
    }

    async with aioresponses() as mocked:
        mocked.get("http://mocked-service-url/api", payload=pyload)
        response = await client.get('/test')
        assert response.status_code == 200

    async with ClientSession() as session:
        async with session.get(
                settings.test_service_url, params=PARAMS_TEST_API
        ) as response:
            assert response.status == 200
            json_data = await response.json()
            assert json_data == pyload
