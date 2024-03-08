from app.resources.queues.google_pubsub_queue import PubSubQueue
from app.resources.repositories import FirestoreCrawlingProcessesRepository
from app.services.crawling_service import CrawlingService
from app.services.html_service import HtmlService


def create_crawl_service():
    return CrawlingService(
        db=FirestoreCrawlingProcessesRepository(),
        queue=PubSubQueue(),
        html_service=HtmlService(),
    )
