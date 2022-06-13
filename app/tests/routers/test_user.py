import pytest
from fastapi.testclient import TestClient

from app.infrastructure.database import get_session
from app.tests.setup_test_db import override_get_session
from server import app

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


@pytest.fixture()
def normal_user_token_in_headers():
    data = {"username": "test1", "password": "Test1@123"}
    response = client.post("/api/v1/login", json=data)
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    yield headers


@pytest.fixture()
def superuser_token_in_headers():
    data = {"username": "admin", "password": "Admin@123"}
    response = client.post("/api/v1/login", json=data)
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    yield headers


def test_login_by_username():
    """
    用户名登录
    """
    data = {"username": "admin", "password": "Admin@123"}
    response = client.post("/api/v1/login", json=data)
    assert response.status_code == 200
    assert response.json()["token"]


def test_login_by_email():
    """
    邮箱登录
    """
    data = {"email": "admin@devops.com", "password": "Admin@123"}
    response = client.post("/api/v1/login", json=data)
    assert response.status_code == 200
    assert response.json()["token"]


def test_login_fail():
    """
    登录失败
    """
    data = {"email": "admin@devops.com", "password": "test123"}
    response = client.post("/api/v1/login", json=data)
    assert response.status_code == 400
    assert response.json()["detail"]


def test_register():
    """
    普通用户注册
    """
    data = {"username": "user01", "password": "User@123", "email": "user@devops.com"}
    response = client.post("/api/v1/register", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert data["username"] == response_data["username"]
    assert data["email"] == response_data["email"]
    assert response_data["is_active"] is True
    assert response_data["is_superuser"] is False


def test_register_username_unique_check():
    """
    普通用户注册失败(用户名重复)
    """
    data = {"username": "user02", "password": "User@123", "email": "user02@devops.com"}
    client.post("/api/v1/register", json=data)
    data = {"username": "user02", "password": "User@123", "email": "user03@devops.com"}
    response = client.post("/api/v1/register", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "该用户已存在"


def test_register_email_unique_check():
    """
    普通用户注册失败(邮箱重复)
    """
    data = {"username": "user03", "password": "User@123", "email": "user03@devops.com"}
    client.post("/api/v1/register", json=data)
    data = {"username": "user04", "password": "User@123", "email": "user03@devops.com"}
    client.post("/api/v1/register", json=data)
    response = client.post("/api/v1/register", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "该用户已存在"


def test_get_users(superuser_token_in_headers):
    response = client.get("/api/v1/users", headers=superuser_token_in_headers)
    assert response.status_code == 200
    assert response.json()


def test_get_user(superuser_token_in_headers):
    user_id = 3
    response = client.get(f"/api/v1/users/{user_id}", headers=superuser_token_in_headers)
    assert response.status_code == 200
    assert response.json()["id"] == 3


def test_get_me(normal_user_token_in_headers):
    response = client.get("/api/v1/users/me", headers=normal_user_token_in_headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == "test1"
    assert response_data["email"] == "test1@devops.com"
    assert response_data["is_superuser"] is False


def test_delete_user(superuser_token_in_headers):
    data = {"username": "user04", "password": "User@123", "email": "user04@devops.com"}
    response = client.post("/api/v1/users", json=data, headers=superuser_token_in_headers)
    user_id = response.json()["id"]
    response = client.delete(f"/api/v1/users/{user_id}", headers=superuser_token_in_headers)
    assert response.status_code == 204
