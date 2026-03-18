import logging
from datetime import datetime, timezone

import scrapy

from content_ingestion_agent.crawler.url_source_factory import get_url_source
from content_ingestion_agent.messaging.factory import get_publisher
from content_ingestion_agent.parser.generic_parser import GenericParser

logger = logging.getLogger(__name__)


class ArticleSpider(scrapy.Spider):
    """Fetches article pages from URLs sourced via MongoDB or a local file."""

    name = "article_spider"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.url_source = get_url_source()
        self.parser = GenericParser()
        self.publisher = get_publisher()

    def start_requests(self):
        """Yield Scrapy Requests for each pending URL."""
        for item in self.url_source.pending_urls():
            yield scrapy.Request(
                url=item.url,
                errback=self.errback,
                # Pass original URL via cb_kwargs so mark_done uses the
                # pre-redirect URL rather than response.url after redirects.
                cb_kwargs={"url": item.url},
            )

    def parse(self, response, url: str):
        """Parse HTML response and publish the resulting Article."""
        fetched_at = datetime.now(timezone.utc)
        article = self.parser.parse(url=url, html=response.text, fetched_at=fetched_at)
        self.publisher.publish(article)
        self.url_source.mark_done(url)

    def errback(self, failure):
        """Mark URL as failed on request error."""
        url = failure.request.url
        self.url_source.mark_failed(url=url, error=repr(failure.value))
        logger.error("Request failed: %s — %s", url, failure.value)
