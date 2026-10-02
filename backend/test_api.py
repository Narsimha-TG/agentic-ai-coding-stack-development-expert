import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2

def test_create_review():
    payload = {
        "id": 3,
        "title": "Verification Gamma",
        "status": "completed",
        "score": 95.0,
        "timestamp": "2023-10-27T10:00:00"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 3
    assert response.json()["title"] == "Verification Gamma"

def test_create_review_invalid():
    payload = {"id": "invalid_id", "title": "Fail"}
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 422