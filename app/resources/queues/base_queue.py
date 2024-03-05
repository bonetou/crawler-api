from app.resources.events.base_event import Event
from abc import ABC, abstractmethod


class IQueue(ABC):
    @abstractmethod
    def publish(self, event: Event):
        pass
