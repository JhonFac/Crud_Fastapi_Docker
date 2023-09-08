import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/auth/",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 201


def test_login_for_access_token():
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200


def test_user():
    response = client.get(
        "/auth/",
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_read_people():
    response = client.get(
        "/people/",
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
