from fastapi import Depends, FastAPI, Request
from app.services import CrawlingService
import pydantic
import logging

logger = logging.getLogger(__name__)

app = FastAPI()


class CreateCrawlRequest(pydantic.BaseModel):
    initial_url: pydantic.AnyUrl


def create_crawl_service():
    return CrawlingService()


@app.post("/crawl")
async def crawl(request: CreateCrawlRequest, service: CrawlingService = Depends(create_crawl_service)):
    return await service.start(str(request.initial_url))


@app.post("/internal/process")
async def process(request: Request):
    pubsub_request = await request.json()
    logger.info(f"Received pubsub request: {pubsub_request}")
    return {"status": "ok"}
