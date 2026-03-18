from typing import Iterator

from content_ingestion_agent.models.url_item import UrlItem


class MongoUrlSource:
    """Reads pending URLs from MongoDB and marks them done/failed after crawling."""

    def __init__(self, uri: str, db: str, collection: str) -> None:
        ...

    def pending_urls(self) -> Iterator[UrlItem]:
        """Yield UrlItems with status=pending, ordered by priority desc."""
        ...

    def mark_done(self, url: str) -> None:
        """Set status=done and crawled_at=now for the given URL."""
        ...

    def mark_failed(self, url: str, error: str) -> None:
        """Set status=failed and record the error message."""
        ...
