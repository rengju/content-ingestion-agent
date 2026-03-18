from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class CrawlStatus(str, Enum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"


class UrlItem(BaseModel):
    url: str
    status: CrawlStatus = CrawlStatus.PENDING
    crawled_at: datetime | None = None
    error: str | None = None
    priority: int = 0
    retry_count: int = 0
    domain: str | None = None
