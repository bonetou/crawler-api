from fastapi import FastAPI
from app.services import CrawlService
import pydantic


app = FastAPI()

class CreateCrawlRequest(pydantic.BaseModel):
    initial_url: pydantic.AnyUrl



@app.post("/crawl")
async def crawl(request: CreateCrawlRequest):
    service = CrawlService()
    return await service.start(request.initial_url)
  
    