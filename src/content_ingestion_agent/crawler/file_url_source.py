import logging
from pathlib import Path
from typing import Iterator

from content_ingestion_agent.crawler.url_source import UrlSource
from content_ingestion_agent.models.url_item import UrlItem

logger = logging.getLogger(__name__)


class FileUrlSource(UrlSource):
    """Reads pending URLs from a plain text file. Used in dev mode.

    File format: one URL per line. Lines starting with '#' and blank lines are ignored.
    mark_done and mark_failed are no-ops — the file has no persistent state to update.
    """

    def __init__(self, feed_file: str) -> None:
        self.feed_file = Path(feed_file)

    def pending_urls(self) -> Iterator[UrlItem]:
        with self.feed_file.open() as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                yield UrlItem(url=line)

    def mark_done(self, url: str) -> None:
        logger.debug("FileUrlSource.mark_done (no-op): %s", url)

    def mark_failed(self, url: str, error: str) -> None:
        logger.debug("FileUrlSource.mark_failed (no-op): url=%s error=%s", url, error)
