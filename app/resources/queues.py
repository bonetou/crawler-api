from abc import ABC, abstractmethod
from enum import StrEnum
from google.cloud import pubsub
import json


class IQueue(ABC):
    @abstractmethod
    def publish(self, topic_name: str, data: dict):
        pass


class PubsubTopics(StrEnum):
    CRAWLING_STARTED = "crawling_started"


class PubSubQueue(IQueue):
    def __init__(self):
        self._client = pubsub.PublisherClient()
        self._project_id = "gcp-project-id"

    def publish(self, topic_name: str, data: dict):
        topic_path = self._client.topic_path(self._project_id, topic_name)
        self._client.publish(topic=topic_path, data=json.dumps(data).encode('utf-8'))
