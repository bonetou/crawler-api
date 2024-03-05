from app.resources.events.base_event import Event
from app.resources.queues.base_queue import IQueue
from google.cloud import pubsub
import json


class PubSubQueue(IQueue):
    def __init__(self):
        self._client = pubsub.PublisherClient()
        self._project_id = "criscon"

    def publish(self, event: Event):
        topic = self._client.topic_path(project=self._project_id, topic=event.name)
        data = json.dumps(event.data.model_dump()).encode("utf-8")
        self._client.publish(topic=topic, data=data)
