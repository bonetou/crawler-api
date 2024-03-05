import pytest
from app.main import app, create_crawl_service
from fastapi.testclient import TestClient
from app.resources.repositories import CrawlingStatus, ProcessNotFoundError

from app.services.crawling_service import CrawlingProcess


class FakeCrawlService:
    def __init__(self, raise_404: bool = False) -> None:
        self.raise_404 = raise_404

    async def start(self, initial_url):
        return CrawlingProcess(
            id="fake-id",
            initial_url=str(initial_url),
            status=CrawlingStatus.CREATED,
        )

    async def get(self, id):
        if self.raise_404:
            raise ProcessNotFoundError
        return CrawlingProcess(
            id="fake-id",
            initial_url="http://example.com/",
            status=CrawlingStatus.CREATED,
        )


def fake_crawl_service():
    return FakeCrawlService()


client = TestClient(app)
app.dependency_overrides[create_crawl_service] = fake_crawl_service


@pytest.mark.asyncio
async def test_should_return_200():
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


@pytest.mark.asyncio
async def test_should_get_crawl():
    app.dependency_overrides[create_crawl_service] = fake_crawl_service
    response = client.get("/crawl/fake-id")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"] == "fake-id"
    assert json_response["initial_url"] == "http://example.com/"
    assert json_response["status"] == "created"
    assert json_response["found_urls"] == []


@pytest.mark.asyncio
async def test_should_return_404_if_crawl_not_found():
    def fake_crawl_service():
        return FakeCrawlService(raise_404=True)

    app.dependency_overrides[create_crawl_service] = fake_crawl_service
    response = client.get("/crawl/invalid-id")
    assert response.status_code == 404
    assert response.json() == {"message": "Process not found"}
