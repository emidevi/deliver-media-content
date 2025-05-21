from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_search_endpoint_success():
    # Basic test with a valid query
    response = client.get("/search?q=berlin&limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) <= 5
    if data:
        item = data[0]
        assert "id" in item
        assert "title" in item
        assert "description" in item
        assert "db" in item

def test_search_empty_query():
    response = client.get("/search")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_search_invalid_limit():
    response = client.get("/search?q=test&limit=1000")
    assert response.status_code == 422 