from app.resources.events.created_process_event import (
    CreatedProcessData,
    CreatedProcessEvent,
)


class EventFactory:
    @classmethod
    def process_created(cls, data: CreatedProcessData) -> CreatedProcessEvent:
        return CreatedProcessEvent(data=data)
