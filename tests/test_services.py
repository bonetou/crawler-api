import pytest
from app.resources.queues import IQueue, PubsubTopics
from app.services import CrawlingService
from app.resources.repositories import CrawlingStatus, ICrawlingProcessesRepository


class FakeRepository(ICrawlingProcessesRepository):
    def __init__(self):
        self.data = []

    async def add(self, data):
        self.data.append(data)
        return data.id


class FakeQueue(IQueue):
    def __init__(self):
        self.data = []

    def publish(self, topic_name, data):
        self.data.append((topic_name, data))


@pytest.mark.asyncio
async def test_should_start_crawling():
    fake_queue = FakeQueue()
    fake_repository = FakeRepository()
    service = CrawlingService(queue=fake_queue, db=fake_repository)
    initial_url = "http://example.com"
    process = await service.start(initial_url)
    dict_process = process.model_dump()

    assert dict_process["id"]
    assert dict_process["initial_url"] == initial_url
    assert dict_process["status"] == CrawlingStatus.pending
    assert dict_process["found_urls"] == []

    assert fake_repository.data == [process]
    assert fake_queue.data == [(PubsubTopics.CRAWLING_STARTED, dict_process)]
