from app.main import app
from fastapi.testclient import TestClient
import pytest


client = TestClient(app)

@pytest.mark.asyncio
async def test_should_start_crawling():
    response = client.post("/crawl", json={"initial_url": "http://example.com/"})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"]
    assert json_response["initial_url"] == "http://example.com/"
    assert json_response["status"] == "pending"
    assert json_response["found_urls"] == []

@pytest.mark.asyncio
async def test_should_return_422_if_invalid_url():
    response = client.post("/crawl", json={"initial_url": "invalid-url"})
    assert response.status_code == 422