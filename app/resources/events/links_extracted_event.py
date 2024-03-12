import pydantic

from app.resources.events.base_event import Event, EventName


class LinksExtractedData(pydantic.BaseModel):
    id: str
    urls: list[str]


class LinksExtractedEvent(Event):
    name: EventName = pydantic.Field(default=EventName.LINKS_EXTRACTED, frozen=True)
    data: LinksExtractedData
