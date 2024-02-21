from src.main import app
from fastapi.testclient import TestClient
import pytest


client = TestClient(app)

@pytest.mark.asyncio
async def test_crawl():
    response = client.post("/crawl")
    assert response.status_code == 200
    assert response.json() == {"message": "Crawling started"}
