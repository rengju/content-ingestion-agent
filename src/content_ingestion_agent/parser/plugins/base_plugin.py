from abc import ABC, abstractmethod
from urllib.parse import urlparse

from content_ingestion_agent.models.article import Article
from content_ingestion_agent.parser.base_parser import BaseParser


class BasePlugin(BaseParser, ABC):
    """Site-specific parser plugin. Overrides GenericParser for known domains."""

    @property
    @abstractmethod
    def domain(self) -> str:
        """The domain this plugin handles, e.g. 'techcrunch.com'."""
        ...

    def can_parse(self, url: str, html: str) -> bool:
        """Returns True when the URL's netloc exactly matches this plugin's domain."""
        return urlparse(url).netloc == self.domain

    @abstractmethod
    def parse(self, url: str, html: str, fetched_at) -> Article:
        ...
