import pydantic

from app.resources.events.base_event import Event, EventName


class CreatedProcessData(pydantic.BaseModel):
    id: str
    initial_url: str


class CreatedProcessEvent(Event):
    name: EventName = pydantic.Field(default=EventName.CRAWLING_STARTED, frozen=True)
    data: CreatedProcessData
