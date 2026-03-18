from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from content_ingestion_agent.models.url_item import CrawlStatus, UrlItem


def test_defaults():
    """A UrlItem with only url set has sensible default values for all other fields."""
    item = UrlItem(url="https://example.com")
    assert item.status == CrawlStatus.PENDING
    assert item.priority == 0
    assert item.retry_count == 0
    assert item.crawled_at is None
    assert item.error is None
    assert item.domain is None


def test_crawl_status_pending_value():
    """CrawlStatus.PENDING has the string value 'pending'."""
    assert CrawlStatus.PENDING == "pending"


def test_crawl_status_done_value():
    """CrawlStatus.DONE has the string value 'done'."""
    assert CrawlStatus.DONE == "done"


def test_crawl_status_failed_value():
    """CrawlStatus.FAILED has the string value 'failed'."""
    assert CrawlStatus.FAILED == "failed"


def test_accepts_all_statuses():
    """UrlItem accepts every CrawlStatus variant without validation error."""
    for status in CrawlStatus:
        item = UrlItem(url="https://example.com", status=status)
        assert item.status == status


def test_rejects_invalid_status():
    """ValidationError is raised for an unrecognised status string."""
    with pytest.raises(ValidationError):
        UrlItem(url="https://example.com", status="unknown")


def test_rejects_missing_url():
    """ValidationError is raised when url is absent."""
    with pytest.raises(ValidationError):
        UrlItem()


def test_accepts_optional_fields():
    """All optional fields are accepted and stored correctly."""
    now = datetime(2026, 3, 17, 20, 30, 0, tzinfo=timezone.utc)
    item = UrlItem(
        url="https://example.com",
        crawled_at=now,
        error="timeout",
        domain="example.com",
        priority=5,
        retry_count=2,
    )
    assert item.crawled_at == now
    assert item.error == "timeout"
    assert item.domain == "example.com"
    assert item.priority == 5
    assert item.retry_count == 2
