from abc import ABC, abstractmethod

from content_ingestion_agent.models.article import Article


class BaseParser(ABC):
    """Extracts a structured Article from raw HTML."""

    @abstractmethod
    def can_parse(self, url: str, html: str) -> bool:
        """Return True if this parser can handle the given URL/HTML."""
        ...

    @abstractmethod
    def parse(self, url: str, html: str, fetched_at) -> Article:
        """Parse HTML and return a validated Article."""
        ...
