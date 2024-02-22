from fastapi import Depends, FastAPI
from app.services import CrawlService
import pydantic


app = FastAPI()

class CreateCrawlRequest(pydantic.BaseModel):
    initial_url: pydantic.AnyUrl


def create_crawl_service():
    return CrawlService()


@app.post("/crawl")
async def crawl(request: CreateCrawlRequest, service: CrawlService = Depends(create_crawl_service)):
    return await service.start(request.initial_url)
