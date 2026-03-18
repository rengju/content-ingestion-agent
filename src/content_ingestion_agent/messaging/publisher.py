from abc import ABC, abstractmethod

from content_ingestion_agent.models.article import Article


class Publisher(ABC):
    @abstractmethod
    def publish(self, article: Article) -> None:
        """Publish a single Article as a message."""
        ...
