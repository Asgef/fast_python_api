from fastapi.testclient import TestClient
from aioresponses import aioresponses
from fast_python_api.main import app
from fast_python_api.settings import settings


client = TestClient(app)


def test_homepage():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'Hello': 'World'}


def test_external_api_test():
    mocked_payload = {
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
        'info': {
            'seed': '25a8adac11c81aa4',
            'results': 5,
            'page': 1,
            'version': '1.4'
        }
    }

    url = settings.test_service_url
    params = settings.param_test_api

    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    full_url = f"{url}?{query_string}"

    with aioresponses() as mock:
        mock.get(
            full_url,
            payload=mocked_payload
        )

        response = client.get("/test")

    assert response.status_code == 200
    data = response.json()
    assert data == mocked_payload
