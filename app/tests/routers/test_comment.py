import time

from fastapi.testclient import TestClient

from app.infrastructure.database import get_session
from app.tests.setup_test_db import override_get_session
from server import app

from .test_user import superuser_token_in_headers, normal_user_token_in_headers

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


def test_get_comments(normal_user_token_in_headers):
    for _ in range(10):
        data = {"content": "测试评论", "parent_id": None}
        response = client.post("/api/v1/comments", json=data, headers=normal_user_token_in_headers)
        for _ in range(50):
            data["parent_id"] = response.json()["id"]
            response = client.post("/api/v1/comments", json=data, headers=normal_user_token_in_headers)
    start = time.time()
    response = client.get("/api/v1/comments")
    end = time.time()
    assert end - start < 0.5  # 读取 50 层嵌套的 10 条评论, 时间应该低于 500 毫秒
    assert response.status_code == 200


def test_get_comment(normal_user_token_in_headers):
    data = {"content": "测试评论"}
    response = client.post("/api/v1/comments", json=data, headers=normal_user_token_in_headers)
    comment_id = response.json()["id"]
    response = client.get(f"/api/v1/comments/{comment_id}", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == comment_id
    assert response_data["content"] == data["content"]


def test_create_comment(normal_user_token_in_headers):
    data = {"content": "测试评论"}
    response = client.post("/api/v1/comments", json=data, headers=normal_user_token_in_headers)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["content"] == data["content"]


def test_delete_comment(superuser_token_in_headers):
    """
    删除评论
    """
    data = {"content": "测试评论"}
    response = client.post("/api/v1/comments", json=data, headers=superuser_token_in_headers)
    comment_id = response.json()["id"]
    response = client.delete(f"/api/v1/comments/{comment_id}", headers=superuser_token_in_headers)
    assert response.status_code == 204
