from fastapi.testclient import TestClient
from extractor.api.app import app

client = TestClient(app)

def test_api_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"

def test_api_benchmark_endpoint():
    response = client.get("/api/v1/benchmark")
    assert response.status_code == 200
    data = response.json()
    assert data["time_reduction_percentage"] > 70.0
