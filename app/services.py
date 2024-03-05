import aiohttp
from bs4 import BeautifulSoup
from app.resources.queues import (
    CreatedCrawlingProcessData,
    CreatedCrawlingProcessEvent,
    IQueue,
    created_crawling_process_event,
)
from app.resources.repositories import (
    CrawlingProcess,
    CrawlingStatus,
    ICrawlingProcessesRepository,
)


class HtmlService:
    async def get_html(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            return await response.text()


class CrawlingService:
    def __init__(
        self, db: ICrawlingProcessesRepository, queue: IQueue, html_service: HtmlService
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
            event=created_crawling_process_event(
                data=CreatedCrawlingProcessData(
                    id=pending_crawling_process.id, initial_url=url
                )
            ),
        )
        return pending_crawling_process

    async def process(self, event: CreatedCrawlingProcessEvent) -> CrawlingProcess:
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
        return link != url and url in link
