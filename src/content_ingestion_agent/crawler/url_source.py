from abc import ABC, abstractmethod
from typing import Iterator

from content_ingestion_agent.models.url_item import UrlItem


class UrlSource(ABC):
    @abstractmethod
    def pending_urls(self) -> Iterator[UrlItem]: ...

    @abstractmethod
    def mark_done(self, url: str) -> None: ...

    @abstractmethod
    def mark_failed(self, url: str, error: str) -> None: ...
