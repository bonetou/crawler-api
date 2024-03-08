from app.resources.repositories.base_repository import (
    ICrawlingProcessesRepository,
    ProcessNotFoundError,
)
from app.resources.model import CrawlingProcess
from google.cloud import firestore


class FirestoreCrawlingProcessesRepository(ICrawlingProcessesRepository):
    collection_name = "crawling-processes"

    def __init__(self):
        self._client = firestore.AsyncClient()
        self._collection = self._client.collection(self.collection_name)

    async def get(self, id: str) -> CrawlingProcess:
        doc_ref = self._collection.document(document_id=id)
        doc = await doc_ref.get()
        if not doc.exists:
            raise ProcessNotFoundError(f"Process with id {id} not found")
        return CrawlingProcess(**doc.to_dict(), id=doc.id)

    async def add(self, data: CrawlingProcess) -> None:
        doc_ref = self._collection.document(document_id=data.id)
        await doc_ref.set(document_data=data.model_dump(exclude={"id"}))
        return doc_ref.id

    async def update(self, data: CrawlingProcess) -> None:
        doc_ref = self._collection.document(document_id=data.id)
        await doc_ref.set(document_data=data.model_dump(exclude={"id"}))
        return doc_ref.id
