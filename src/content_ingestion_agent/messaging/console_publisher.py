import logging

from content_ingestion_agent.messaging.publisher import Publisher
from content_ingestion_agent.models.article import Article

logger = logging.getLogger(__name__)


class ConsolePublisher(Publisher):
    """Publisher that logs Article JSON to the console. Used in dev mode."""

    def publish(self, article: Article) -> None:
        logger.info("[CONSOLE PUBLISHER] %s", article.model_dump_json())
