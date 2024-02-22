from fastapi import Depends, FastAPI
from app.services import CrawlingService
import pydantic


app = FastAPI()

class CreateCrawlRequest(pydantic.BaseModel):
    initial_url: pydantic.AnyUrl


def create_crawl_service():
    return CrawlingService()


@app.post("/crawl")
async def crawl(request: CreateCrawlRequest, service: CrawlingService = Depends(create_crawl_service)):
    return await service.start(str(request.initial_url))
