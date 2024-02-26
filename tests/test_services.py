import pytest
from app.resources.queues import IQueue, PubsubTopics
from app.services import CrawlingService, HtmlService
from app.resources.repositories import CrawlingProcess, CrawlingStatus, ICrawlingProcessesRepository


class FakeHtmlService(HtmlService):
    def __init__(self, html=str):
        self.html = html
    
    async def get_html(self, url: str) -> str:
        return self.html


class FakeRepository(ICrawlingProcessesRepository):
    def __init__(self):
        self.data = []

    async def get(self, id):
        return self.data[0]
    
    async def add(self, data):
        self.data.append(data)
        return data.id

    async def update(self, data):
        self.data = [data]
    

class FakeQueue(IQueue):
    def __init__(self):
        self.data = []

    def publish(self, topic_name, data):
        self.data.append((topic_name, data))


@pytest.mark.asyncio
async def test_should_start_crawling():
    fake_queue = FakeQueue()
    fake_repository = FakeRepository()
    fake_html_service = FakeHtmlService()
    service = CrawlingService(queue=fake_queue, db=fake_repository, html_service=fake_html_service)
    initial_url = "http://example.com"
    process = await service.start(initial_url)

    assert process.id
    assert process.initial_url == initial_url
    assert process.status == CrawlingStatus.IN_PROGRESS
    assert process.found_urls == []

    assert fake_repository.data == [process]
    assert fake_queue.data == [(PubsubTopics.CRAWLING_STARTED, process.model_dump())]


@pytest.mark.asyncio
async def test_should_extract_urls_when_processing():
    fake_queue = FakeQueue()
    fake_repository = FakeRepository()
    fake_html_service = FakeHtmlService('''
        <html><a href='http://example.com/link1'></a><a href='http://example.com/link2'></a></html>'''
    )
    service = CrawlingService(queue=fake_queue, db=fake_repository, html_service=fake_html_service)
    current_process = CrawlingProcess(id="123", initial_url="http://example.com", status=CrawlingStatus.IN_PROGRESS)
    process = await service.process(current_process)
    
    assert process.id == "123"
    assert process.status == CrawlingStatus.COMPLETED
    assert process.found_urls == ["http://example.com/link1", "http://example.com/link2"]



@pytest.mark.asyncio
async def test_should_return_empty_list_if_no_links():
    fake_queue = FakeQueue()
    fake_repository = FakeRepository()
    fake_html_service = FakeHtmlService('<html></html>')
    service = CrawlingService(queue=fake_queue, db=fake_repository, html_service=fake_html_service)
    current_process = CrawlingProcess(id="123", initial_url="http://example.com", status=CrawlingStatus.IN_PROGRESS)
    process = await service.process(current_process)
    assert process.found_urls == []
