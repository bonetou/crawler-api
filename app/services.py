import aiohttp
from bs4 import BeautifulSoup
from app.resources.queues import IQueue, PubsubTopics
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
    def __init__(self, db: ICrawlingProcessesRepository, queue: IQueue, html_service: HtmlService):
        self._db = db
        self._queue = queue
        self._html_service = html_service

    async def get(self, id: str) -> CrawlingProcess:
        return await self._db.get(id=id)

    async def start(self, url: str) -> CrawlingProcess:
        pending_crawling_process = CrawlingProcess(initial_url=url, status=CrawlingStatus.IN_PROGRESS)
        await self._db.add(data=pending_crawling_process)
        self._queue.publish(topic_name=PubsubTopics.CRAWLING_STARTED, data=pending_crawling_process.model_dump())
        return pending_crawling_process

    async def process(self, crawling_process: CrawlingProcess) -> CrawlingProcess:
        html = await self._html_service.get_html(url=crawling_process.initial_url)
        links = self._get_links(html, url=crawling_process.initial_url)
        crawling_process.status = CrawlingStatus.COMPLETED
        crawling_process.found_urls = links
        await self._db.update(data=crawling_process)
        return crawling_process

    def _get_links(self, html: str, url: str) -> list:
        soup = BeautifulSoup(html, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        return [link for link in links if self._is_link_valid(link=link, url=url)]

    def _is_link_valid(self, link: str, url: str) -> bool:
        return link != url and link.startswith(url)
