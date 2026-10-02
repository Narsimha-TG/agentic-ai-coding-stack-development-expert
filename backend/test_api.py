import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_nodes" in data
    assert "avg_score" in data
    assert isinstance(data["total_nodes"], int)

def test_create_review():
    payload = {
        "id": 3,
        "title": "Cloud Node Gamma",
        "status": "active",
        "score": 95.0,
        "timestamp": "2023-10-27T10:00:00"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json() == payload

def test_create_review_invalid():
    # Testing schema validation failure
    payload = {"id": "not-an-int", "title": "Invalid"}
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 422