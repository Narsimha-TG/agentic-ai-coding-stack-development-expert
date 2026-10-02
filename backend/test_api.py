import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "workers": "active"}

def test_process_novel_success():
    payload = {
        "title": "The Great Gatsby",
        "lang": "en-US",
        "voice_id": "voice-001"
    }
    response = client.post("/api/v1/process-novel", params=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["novel_title"] == "The Great Gatsby"
    assert "task_id" in data
    assert data["status"] == "pending"

def test_get_task_not_found():
    response = client.get("/api/v1/tasks/non-existent-id")
    assert response.status_code == 404

def test_translate_endpoint():
    # First create a task
    create_res = client.post("/api/v1/process-novel", params={"title": "Test", "lang": "fr", "voice_id": "v1"})
    task_id = create_res.json()["task_id"]
    
    # Trigger translation
    response = client.post(f"/api/v1/translate?task_id={task_id}&chapter_index=1")
    assert response.status_code == 200
    assert "Translation triggered" in response.json()["message"]