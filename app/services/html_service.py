from abc import ABC
import aiohttp


class IHtmlService(ABC):
    async def get_html(self, url: str) -> str:
        pass


class HtmlService(IHtmlService):
    async def get_html(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            return await response.text()
