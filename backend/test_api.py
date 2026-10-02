import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_get_metrics():
    response = client.get("/api/v1/dashboard/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_items" in data
    assert "avg_score" in data
    assert data["status"] == "healthy"

def test_execute_action():
    payload = {"action": "restart", "target_id": 1}
    response = client.post("/api/v1/dashboard/actions", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["action_received"] == payload

def test_get_data_feed():
    response = client.get("/api/v1/dashboard/data-feed?page=1&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if len(response.json()) > 0:
        item = response.json()[0]
        assert "id" in item
        assert "title" in item
        assert "status" in item