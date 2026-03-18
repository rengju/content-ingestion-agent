from abc import ABC, abstractmethod

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
        """Returns True when the URL's domain matches this plugin's domain."""
        ...

    @abstractmethod
    def parse(self, url: str, html: str, fetched_at) -> Article:
        ...
