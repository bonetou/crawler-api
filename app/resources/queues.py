from abc import ABC, abstractmethod
from enum import StrEnum
from google.cloud import pubsub
import json
import pydantic


class EventNames(StrEnum):
    CRAWLING_STARTED = "crawling-started"


class Event(pydantic.BaseModel):
    name: EventNames
    data: dict


class CreatedCrawlingProcessData(pydantic.BaseModel):
    id: str
    initial_url: str


class CreatedCrawlingProcessEvent(Event):
    name: EventNames = EventNames.CRAWLING_STARTED
    data: CreatedCrawlingProcessData


def created_crawling_process_event(
    data: CreatedCrawlingProcessData,
) -> CreatedCrawlingProcessEvent:
    return CreatedCrawlingProcessEvent(data=data)


class IQueue(ABC):
    @abstractmethod
    def publish(self, event: Event):
        pass


class PubSubQueue(IQueue):
    def __init__(self):
        self._client = pubsub.PublisherClient()
        self._project_id = "criscon"

    def publish(self, event: Event):
        topic_path = self._client.topic_path(project=self._project_id, topic=event.name)
        self._client.publish(
            topic=topic_path, data=json.dumps(event.data).encode("utf-8")
        )
