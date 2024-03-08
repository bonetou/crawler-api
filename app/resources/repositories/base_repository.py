from app.resources.model import CrawlingProcess


from abc import ABC, abstractmethod


class ICrawlingProcessesRepository(ABC):
    @abstractmethod
    async def add(self, data: CrawlingProcess) -> None:
        pass

    @abstractmethod
    async def get(self, id: str) -> CrawlingProcess:
        pass

    @abstractmethod
    async def update(self, data: CrawlingProcess) -> None:
        pass


class ProcessNotFoundError(Exception):
    pass
