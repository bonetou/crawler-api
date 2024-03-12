from enum import StrEnum
import pydantic


class EventName(StrEnum):
    CRAWLING_STARTED = "crawling-started"
    LINKS_EXTRACTED = "links-extracted"


class Event(pydantic.BaseModel):
    name: EventName
    data: pydantic.BaseModel
