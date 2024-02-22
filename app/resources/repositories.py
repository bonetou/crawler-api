from abc import ABC, abstractmethod
from enum import StrEnum
from uuid import uuid4
from google.cloud import firestore
import pydantic


class CrawlingStatus(StrEnum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class CrawlingProcess(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: str(uuid4()))
    initial_url: str
    status: CrawlingStatus
    found_urls: list[str] = []
    crawled_urls: list[str] = []


class ICrawlingProcessesRepository(ABC):
    @abstractmethod
    async def add(self, data: CrawlingProcess) -> None:
        pass


class FirestoreCrawlingProcessesRepository(ICrawlingProcessesRepository):
    collection_name = "crawling_processes"

    def __init__(self):
        self._client = firestore.AsyncClient()
        self._collection = self._client.collection(self.collection_name)
    
    async def add(self, data: CrawlingProcess) -> None:
        doc_ref = self._client.collection("crawling_processes").document(document_id=data.id)
        await doc_ref.set(document_data=data.model_dump(exclude={"id"}))
        return doc_ref.id
