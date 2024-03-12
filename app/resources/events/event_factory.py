from app.resources.events.created_process_event import (
    CreatedProcessData,
    CreatedProcessEvent,
)

from app.resources.events.links_extracted_event import (
    LinksExtractedData,
    LinksExtractedEvent,
)


class EventFactory:
    @classmethod
    def process_created(cls, data: CreatedProcessData) -> CreatedProcessEvent:
        return CreatedProcessEvent(data=data)

    @classmethod
    def links_extracted(cls, data: LinksExtractedData) -> CreatedProcessEvent:
        return LinksExtractedEvent(data=data)
