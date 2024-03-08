from enum import StrEnum
from uuid import uuid4
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
