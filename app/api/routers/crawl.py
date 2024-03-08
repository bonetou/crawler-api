from fastapi import APIRouter, Depends, status, responses
from app.api.deps import create_crawl_service
from app.resources.repositories import (
    ProcessNotFoundError,
)
from app.services.crawling_service import CrawlingService
import pydantic
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/crawl",
    tags=["crawl"],
)


class CreateCrawlRequest(pydantic.BaseModel):
    initial_url: pydantic.AnyUrl


@router.post("/")
async def crawl(
    request: CreateCrawlRequest,
    service: CrawlingService = Depends(create_crawl_service),
):
    return await service.start(str(request.initial_url))


@router.get("/{id}")
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
