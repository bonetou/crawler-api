from enum import StrEnum
from uuid import uuid4
import pydantic

class CrawlStatus(StrEnum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class CrawlingProcess(pydantic.BaseModel):
    id: pydantic.UUID4 = pydantic.Field(default_factory=uuid4)
    initial_url: str
    status: CrawlStatus = CrawlStatus.pending
    found_urls: list[str] = []
    crawled_urls: list[str] = []


class CrawlService:
    def __init__(self):
        pass

    async def start(self, url: pydantic.AnyUrl) -> CrawlingProcess:
        return CrawlingProcess(initial_url=str(url))
