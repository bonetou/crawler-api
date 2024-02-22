from enum import StrEnum
from uuid import uuid4
import pydantic
from google.cloud import firestore, pubsub


class CrawlStatus(StrEnum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class CrawlingProcess(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: str(uuid4()))
    initial_url: str
    status: CrawlStatus = CrawlStatus.pending
    found_urls: list[str] = []
    crawled_urls: list[str] = []


class PubsubTopics(StrEnum):
    CRAWLING_STARTED = "crawling_started"


class FirestoreCollections(StrEnum):
    CRAWLING_PROCESSES = "crawling_processes"


PROJECT_ID = "gcp-project-id"


class CrawlService:
    def __init__(self, db = None, queue = None):
        self._db = db or firestore.AsyncClient()
        self._queue = queue or pubsub.PublisherClient()

    async def start(self, url: pydantic.AnyUrl) -> CrawlingProcess:
        process = CrawlingProcess(initial_url=str(url))
        doc_ref = self._db.collection(FirestoreCollections.CRAWLING_PROCESSES).document(process.id)
        await doc_ref.set(process.model_dump())
        self._publish_to_queue(process, PubsubTopics.CRAWLING_STARTED)
        return process

    def _publish_to_queue(self, process: CrawlingProcess, topic: PubsubTopics):
        topic_path = self._queue.topic_path(PROJECT_ID, topic)
        self._queue.publish(topic=topic_path, data=process.model_dump_json().encode('utf-8'))
