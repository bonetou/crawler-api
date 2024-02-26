from app.main import app, create_crawl_service
from fastapi.testclient import TestClient
import pytest
from app.resources.repositories import CrawlingStatus

from app.services import CrawlingProcess

class FakeCrawlService:
    async def start(self, initial_url):
        return CrawlingProcess(
            id="fake-id",
            initial_url=str(initial_url),
            status=CrawlingStatus.CREATED,
        )

def fake_crawl_service():
    return FakeCrawlService()


client = TestClient(app)

@pytest.mark.asyncio
async def test_should_return_200():
    app.dependency_overrides[create_crawl_service] = fake_crawl_service
    response = client.post("/crawl", json={"initial_url": "http://example.com/"})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"] == "fake-id"
    assert json_response["initial_url"] == "http://example.com/"
    assert json_response["status"] == "created"
    assert json_response["found_urls"] == []


@pytest.mark.asyncio
async def test_should_return_422_if_invalid_url():
    response = client.post("/crawl", json={"initial_url": "invalid-url"})
    assert response.status_code == 422