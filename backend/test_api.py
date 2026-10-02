import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_health():
    # Note: The provided implementation does not have a root path, 
    # but we test the existing endpoints for health/status.
    response = client.get("/api/v1/reports/daily")
    assert response.status_code == 200

def test_daily_report_metrics():
    response = client.get("/api/v1/reports/daily")
    assert response.status_code == 200
    assert "total_sales" in response.json()

def test_create_transaction_valid():
    payload = {
        "transaction_id": "TXN-12345",
        "total_amount": 99.99,
        "tax_details": {"GST": 5.0, "QST": 9.97}
    }
    response = client.post("/api/v1/transactions", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction processed"
    assert response.json()["id"] == "TXN-12345"

def test_srm_sign_endpoint():
    payload = {"data": {"amount": 100}}
    response = client.post("/api/v1/srm/sign", json=payload)
    assert response.status_code == 200
    assert "srm_signature" in response.json()
    assert response.json()["status"] == "signed"