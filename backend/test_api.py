import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_data():
    response = client.get("/api/data/export")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_trigger_scrape_valid():
    payload = {"url": "https://example.com/product/123"}
    response = client.post("/api/scrape/trigger", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Scraping job initiated"
    assert data["url"] == payload["url"]
    assert "job_id" in data

def test_update_theme_valid():
    payload = {"theme": "dark", "toggle_bg_color": "#000000"}
    response = client.patch("/api/settings/theme", json=payload)
    assert response.status_code == 200
    assert response.json()["settings"] == payload