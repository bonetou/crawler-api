from app.resources.queues import IQueue, PubSubQueue, PubsubTopics
from app.resources.repositories import (
    CrawlingProcess,
    CrawlingStatus,
    FirestoreCrawlingProcessesRepository,
    ICrawlingProcessesRepository,
)

class CrawlingService:
    def __init__(self, db: ICrawlingProcessesRepository | None = None, queue: IQueue | None = None):
        self._db = db or FirestoreCrawlingProcessesRepository()
        self._queue = queue or PubSubQueue()

    async def start(self, url: str) -> CrawlingProcess:
        pending_crawling_process = CrawlingProcess(initial_url=url, status=CrawlingStatus.pending)
        await self._db.add(data=pending_crawling_process)
        self._queue.publish(topic_name=PubsubTopics.CRAWLING_STARTED, data=pending_crawling_process.model_dump())
        return pending_crawling_process
