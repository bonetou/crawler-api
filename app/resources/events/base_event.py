from enum import StrEnum
import pydantic


class EventName(StrEnum):
    CRAWLING_STARTED = "crawling-started"


class Event(pydantic.BaseModel):
    name: EventName
    data: pydantic.BaseModel
