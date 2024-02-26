from abc import ABC, abstractmethod
from enum import StrEnum
from uuid import uuid4
from google.cloud import firestore
import pydantic


class CrawlingStatus(StrEnum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class CrawlingProcess(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: str(uuid4()), frozen=True)
    initial_url: str
    status: CrawlingStatus
    found_urls: list[str] = []


class ICrawlingProcessesRepository(ABC):
    @abstractmethod
    async def add(self, data: CrawlingProcess) -> None:
        pass

    @abstractmethod
    async def get(self, id: str) -> CrawlingProcess:
        pass

    @abstractmethod
    async def update(self, data: CrawlingProcess) -> None:
        pass


class FirestoreCrawlingProcessesRepository(ICrawlingProcessesRepository):
    collection_name = "crawling-processes"

    def __init__(self):
        self._client = firestore.AsyncClient()
        self._collection = self._client.collection(self.collection_name)
    
    async def get(self, id: str) -> CrawlingProcess:
        doc_ref = self._collection.document(document_id=id)
        doc = await doc_ref.get()
        return CrawlingProcess(**doc.to_dict(), id=doc.id)

    async def add(self, data: CrawlingProcess) -> None:
        doc_ref = self._collection.document(document_id=data.id)
        await doc_ref.set(document_data=data.model_dump(exclude={"id"}))
        return doc_ref.id

    async def update(self, data: CrawlingProcess) -> None:
        doc_ref = self._collection.document(document_id=data.id)
        await doc_ref.set(document_data=data.model_dump(exclude={"id"}))
        return doc_ref.id
