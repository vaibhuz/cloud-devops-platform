import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "success"

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_inventory():
    client = app.test_client()
    response = client.get("/api/v1/inventory")
    assert response.status_code == 200
    assert response.json["service"] == "Inventory API"
    assert len(response.json["items"]) == 2
