import base64
import json
from fastapi import Depends, FastAPI, status, responses
from app.resources.queues import CreatedCrawlingProcessEvent, PubSubQueue
from app.resources.repositories import (
    FirestoreCrawlingProcessesRepository,
    ProcessNotFoundError,
)
from app.services.crawling_service import CrawlingService
from app.services.html_service import HtmlService
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

    def decode_data(self) -> dict:
        return json.loads(base64.b64decode(self.message.data).decode("utf-8"))


def create_crawl_service():
    return CrawlingService(
        db=FirestoreCrawlingProcessesRepository(),
        queue=PubSubQueue(),
        html_service=HtmlService(),
    )


@app.post("/crawl")
async def crawl(
    request: CreateCrawlRequest,
    service: CrawlingService = Depends(create_crawl_service),
):
    return await service.start(str(request.initial_url))


@app.get("/crawl/{id}")
async def get_crawl(id: str, service: CrawlingService = Depends(create_crawl_service)):
    try:
        return await service.get(id)
    except ProcessNotFoundError as e:
        logger.error(e)
        return responses.JSONResponse(
            content={"message": "Process not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.error(e)
        return responses.JSONResponse(
            content={"message": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@app.post("/internal/process")
async def process(
    request: PubSubRequest, service: CrawlingService = Depends(create_crawl_service)
):
    process = await service.process(
        event=CreatedCrawlingProcessEvent(data=request.decode_data())
    )
    return process
