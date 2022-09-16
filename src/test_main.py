from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_cities_list():
    response = client.get('/cities/')
    print(response.json())
    assert response.status_code == 200


def test_users_list():
    response = client.get('/users/')
    assert response.status_code == 200


def test_picnics_list():
    response = client.get('/picnics/')
    assert response.status_code == 200
