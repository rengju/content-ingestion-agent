from datetime import datetime

from content_ingestion_agent.models.article import Article
from content_ingestion_agent.parser.base_parser import BaseParser


class GenericParser(BaseParser):
    """Trafilatura-based generic parser. Used as the default/fallback."""

    PARSER_NAME = "generic_trafilatura"

    def can_parse(self, url: str, html: str) -> bool:
        """Always returns True — this is the catch-all fallback parser."""
        ...

    def parse(self, url: str, html: str, fetched_at: datetime) -> Article:
        """Extract article content using Trafilatura, return Article."""
        ...
