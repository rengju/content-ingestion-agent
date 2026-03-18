from datetime import date, datetime
from urllib.parse import urlparse

import trafilatura

from content_ingestion_agent.models.article import Article
from content_ingestion_agent.parser.base_parser import BaseParser


class GenericParser(BaseParser):
    """Trafilatura-based generic parser. Used as the default/fallback."""

    PARSER_NAME = "generic_trafilatura"

    def can_parse(self, url: str, html: str) -> bool:
        """Always returns True — this is the catch-all fallback parser."""
        return True

    def parse(self, url: str, html: str, fetched_at: datetime) -> Article:
        """Extract article content using Trafilatura, return Article."""
        doc = trafilatura.bare_extraction(html, url=url, include_comments=False)
        result = doc.as_dict() if doc is not None else {}

        raw_date = result.get("date")
        parsed_date = date.fromisoformat(raw_date) if raw_date else None

        return Article(
            url=url,
            source=urlparse(url).netloc,
            title=result.get("title") or "",
            date=parsed_date,
            author=result.get("author"),
            text=result.get("text") or "",
            fetched_at=fetched_at,
            parser_used=self.PARSER_NAME,
        )
