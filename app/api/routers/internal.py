import base64
import json
from fastapi import Depends, APIRouter
from app.api.deps import create_crawl_service, screenshot_service
from app.resources.events.created_process_event import CreatedProcessEvent
from app.resources.events.links_extracted_event import LinksExtractedEvent

from app.services.crawling_service import CrawlingService
import pydantic

from app.services.screenshot_service import ScreenshotService

router = APIRouter(
    prefix="/internal",
    tags=["internal"],
)


class CreateCrawlRequest(pydantic.BaseModel):
    initial_url: pydantic.AnyUrl


class PubsubMessage(pydantic.BaseModel):
    data: str


class PubSubRequest(pydantic.BaseModel):
    message: PubsubMessage

    def decode_data(self) -> dict:
        return json.loads(base64.b64decode(self.message.data).decode("utf-8"))


@router.post("/extract_links")
async def process(
    request: PubSubRequest, service: CrawlingService = Depends(create_crawl_service)
):
    process = await service.extract_links(
        event=CreatedProcessEvent(data=request.decode_data())
    )
    return process


@router.post("/screenshot")
async def screenshot(
    request: PubSubRequest, service: ScreenshotService = Depends(screenshot_service)
):
    event = LinksExtractedEvent(data=request.decode_data())
    await service.take_screenshot(event=event)
    return {"status": "ok"}
