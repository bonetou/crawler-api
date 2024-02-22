import pytest
from unittest.mock import Mock
from app.services import CrawlService
from google.cloud import firestore


@pytest.mark.asyncio
async def test_should_start_crawling():
    queue_mock = Mock(topic_path=Mock(return_value="projects/gcp-project-id/topics/crawling_started"))
    service = CrawlService(queue=queue_mock)
    process = await service.start("http://example.com")
    dict_process = process.model_dump()
    assert dict_process["id"]
    assert dict_process["initial_url"] == "http://example.com"
    assert dict_process["status"] == "pending"
    assert dict_process["found_urls"] == []

    db = firestore.AsyncClient()
    doc_ref = db.collection("crawling_processes").document(process.id)
    doc = await doc_ref.get()
    assert doc.to_dict() == dict_process

    queue_mock.publish.assert_called_once_with(
        topic="projects/gcp-project-id/topics/crawling_started",
        data=process.model_dump_json().encode("utf-8"),
    )
