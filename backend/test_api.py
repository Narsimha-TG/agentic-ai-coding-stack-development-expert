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
    data = response.json()
    assert "total_items" in data
    assert "average_score" in data
    assert isinstance(data["total_items"], int)

def test_create_review():
    payload = {
        "id": 3,
        "title": "Box Design C",
        "status": "pending",
        "score": 90.0,
        "timestamp": "2023-10-27T10:00:00"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Box Design C"
    
    # Verify it was added by checking analytics count
    analytics = client.get("/api/analytics").json()
    assert analytics["total_items"] == 3