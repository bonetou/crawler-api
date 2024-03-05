from bs4 import BeautifulSoup
from app.resources.events.event_factory import EventFactory
from app.resources.events.created_process_event import CreatedProcessData
from app.resources.queues.base_queue import (
    IQueue,
)
from app.resources.repositories import (
    CrawlingProcess,
    CrawlingStatus,
    ICrawlingProcessesRepository,
)
from urllib.parse import urlparse
from app.services.html_service import IHtmlService


class CrawlingService:
    def __init__(
        self,
        db: ICrawlingProcessesRepository,
        queue: IQueue,
        html_service: IHtmlService,
    ):
        self._db = db
        self._queue = queue
        self._html_service = html_service

    async def get(self, id: str) -> CrawlingProcess:
        return await self._db.get(id=id)

    async def start(self, url: str) -> CrawlingProcess:
        pending_crawling_process = CrawlingProcess(
            initial_url=url, status=CrawlingStatus.IN_PROGRESS
        )
        await self._db.add(data=pending_crawling_process)
        self._queue.publish(
            event=EventFactory.process_created(
                data=CreatedProcessData(id=pending_crawling_process.id, initial_url=url)
            ),
        )
        return pending_crawling_process

    async def extract_links(self, event: CreatedProcessData) -> CrawlingProcess:
        process = await self._db.get(id=event.data.id)
        html = await self._html_service.get_html(url=event.data.initial_url)
        links = self._get_links(html, url=event.data.initial_url)
        process.found_urls = links
        process.status = CrawlingStatus.COMPLETED
        await self._db.update(data=process)
        return process

    def _get_links(self, html: str, url: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        links = [link.get("href") for link in soup.find_all("a")]
        return [link for link in links if self._is_link_valid(link=link, url=url)]

    def _is_link_valid(self, link: str, url: str) -> bool:
        return link != url and urlparse(link).netloc == urlparse(url).netloc
