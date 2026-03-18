import scrapy

from content_ingestion_agent.crawler.mongo_url_source import MongoUrlSource


class ArticleSpider(scrapy.Spider):
    """Fetches article pages from URLs sourced in MongoDB."""

    name = "article_spider"

    def __init__(self, url_source: MongoUrlSource, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.url_source = url_source

    def start_requests(self):
        """Yield Scrapy Requests for each pending URL."""
        ...

    def parse(self, response):
        """Hand raw HTML response off to the parser pipeline."""
        ...

    def errback(self, failure):
        """Mark URL as failed in MongoDB on request error."""
        ...
