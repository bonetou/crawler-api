import pytest
from app.resources.queues import IQueue, created_crawling_process_event
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

    def publish(self, event):
        self.data.append((event))


@pytest.fixture
def repository_with_process():
    fake_repository = FakeRepository()
    fake_repository.data = [CrawlingProcess(id="123", initial_url="http://example.com", status=CrawlingStatus.IN_PROGRESS)]
    return fake_repository


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
    assert fake_queue.data == [created_crawling_process_event(data={"id": process.id, "initial_url": initial_url})]


@pytest.mark.asyncio
async def test_should_extract_urls_when_processing(repository_with_process):
    fake_queue = FakeQueue()
    fake_html_service = FakeHtmlService('''
        <html><a href='http://example.com/link1'></a><a href='http://example.com/link2'></a></html>'''
    )
    service = CrawlingService(queue=fake_queue, db=repository_with_process, html_service=fake_html_service)
    event = created_crawling_process_event(data={'id': '123', 'initial_url': 'http://example.com'})
    process = await service.process(event)
    
    assert process.id == "123"
    assert process.status == CrawlingStatus.COMPLETED
    assert process.found_urls == ["http://example.com/link1", "http://example.com/link2"]



@pytest.mark.asyncio
async def test_should_return_empty_list_if_no_links(repository_with_process):
    fake_queue = FakeQueue()
    fake_html_service = FakeHtmlService('<html></html>')
    service = CrawlingService(queue=fake_queue, db=repository_with_process, html_service=fake_html_service)
    event = created_crawling_process_event(data={'id': '123', 'initial_url': 'http://example.com'})
    process = await service.process(event)
    assert process.found_urls == []


@pytest.mark.asyncio
async def test_should_not_return_same_url(repository_with_process):
    fake_queue = FakeQueue()
    fake_html_service = FakeHtmlService('<html><a href="http://example.com"></a></html>')
    service = CrawlingService(queue=fake_queue, db=repository_with_process, html_service=fake_html_service)
    event = created_crawling_process_event(data={'id': '123', 'initial_url': 'http://example.com'})
    process = await service.process(event)
    assert process.found_urls == []


@pytest.mark.asyncio
async def test_should_not_return_external_links(repository_with_process):
    fake_queue = FakeQueue()
    fake_html_service = FakeHtmlService('<html><a href="http://external.com"></a></html>')
    service = CrawlingService(queue=fake_queue, db=repository_with_process, html_service=fake_html_service)
    event = created_crawling_process_event(data={'id': '123', 'initial_url': 'http://example.com'})
    process = await service.process(event)
    assert process.found_urls == []
