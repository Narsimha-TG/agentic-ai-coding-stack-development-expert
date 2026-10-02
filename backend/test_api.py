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
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "id" in response.json()[0]
    assert "score" in response.json()[0]

def test_toggle_theme_success():
    payload = {"theme_preference": "dark"}
    response = client.post("/api/theme/toggle", json=payload)
    assert response.status_code == 200
    assert response.json()["current_theme"] == "dark"

def test_toggle_theme_invalid_payload():
    # Testing schema validation
    response = client.post("/api/theme/toggle", json={})
    assert response.status_code == 422