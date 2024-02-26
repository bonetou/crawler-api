import base64
import json
from fastapi import Depends, FastAPI
from app.resources.queues import PubSubQueue
from app.resources.repositories import CrawlingProcess, FirestoreCrawlingProcessesRepository
from app.services import CrawlingService, HtmlService
import pydantic
import logging

logger = logging.getLogger(__name__)

app = FastAPI()


class CreateCrawlRequest(pydantic.BaseModel):
    initial_url: pydantic.AnyUrl

class PubsubMessage(pydantic.BaseModel):
    data: str


class PubSubRequest(pydantic.BaseModel):
    message: PubsubMessage

    def decode_data(self):
        return json.loads(base64.b64decode(self.message.data).decode("utf-8"))


def create_crawl_service():
    return CrawlingService(
        db=FirestoreCrawlingProcessesRepository(),
        queue=PubSubQueue(),
        html_service=HtmlService(),
    )


@app.post("/crawl")
async def crawl(request: CreateCrawlRequest, service: CrawlingService = Depends(create_crawl_service)):
    return await service.start(str(request.initial_url))


@app.post("/internal/process")
async def process(request: PubSubRequest, service: CrawlingService = Depends(create_crawl_service)):
    process = await service.process(CrawlingProcess(**request.decode_data()))
    return process
