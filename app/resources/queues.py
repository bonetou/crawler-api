from abc import ABC, abstractmethod
from enum import StrEnum
from google.cloud import pubsub
import json


class IQueue(ABC):
    @abstractmethod
    def publish(self, topic_name: str, data: dict):
        pass


class PubsubTopics(StrEnum):
    CRAWLING_STARTED = "crawling-started"


class PubSubQueue(IQueue):
    def __init__(self):
        self._client = pubsub.PublisherClient()
        self._project_id = "criscon"

    def publish(self, topic_name: str, data: dict):
        topic_path = self._client.topic_path(project=self._project_id, topic=topic_name)
        self._client.publish(topic=topic_path, data=json.dumps(data).encode('utf-8'))
