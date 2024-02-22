import pytest
from app.services import CrawlService

@pytest.mark.asyncio
async def test_should_start_crawling():
    service = CrawlService()
    process = await service.start("http://example.com")
    dict_process = process.model_dump()
    assert dict_process["id"]
    assert dict_process["initial_url"] == "http://example.com"
    assert dict_process["status"] == "pending"
    assert dict_process["found_urls"] == []


