from app.app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "running"

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_inventory():
    client = app.test_client()
    response = client.get("/api/v1/inventory")
    assert response.status_code == 200
    assert isinstance(response.json, list)
