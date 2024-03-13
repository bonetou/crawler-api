from uuid import uuid4
import pyppeteer
from google.cloud import storage

from app.resources.events.links_extracted_event import LinksExtractedEvent
from app.resources.model import Screeshot
from app.resources.repositories.base_repository import ICrawlingProcessesRepository


class ScreenshotService:
    def __init__(self, repository: ICrawlingProcessesRepository):
        self._repository = repository

    async def take_screenshot(self, event: LinksExtractedEvent) -> str:
        browser = await pyppeteer.launch(headless=True, args=["--no-sandbox"])

        page = await browser.newPage()
        screenshots = []

        for url in event.data.urls:
            await page.goto(url)
            screenshot_bytes = await page.screenshot(fullPage=True)
            screenshot_url = self._save_screenshot(screenshot_bytes, uuid4())
            screenshots.append(Screeshot(url=url, path=screenshot_url))

        process = await self._repository.get(id=event.data.id)
        process.screenshots = screenshots
        await self._repository.update(data=process)
        await browser.close()
        return screenshot_url

    def _save_screenshot(self, screenshot: bytes, filename: str) -> str:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket("crawling-screenshots")
        blob = bucket.blob(f"{filename}.png")
        blob.upload_from_string(screenshot)
        return blob.public_url
