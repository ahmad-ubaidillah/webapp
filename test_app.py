"""Tests for webapp API."""

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_users_unauthorized(client):
    response = client.get("/api/users")
    assert response.status_code == 401


def test_get_posts_empty(client):
    response = client.get("/api/posts")
    assert response.status_code == 200
    assert response.json == []
