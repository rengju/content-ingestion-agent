import logging
import os

from google.cloud import pubsub_v1

from content_ingestion_agent.messaging.publisher import Publisher
from content_ingestion_agent.models.article import Article

logger = logging.getLogger(__name__)


class PubSubPublisher(Publisher):
    def __init__(self):
        self.topic = os.environ["PUBSUB_TOPIC"]
        self.dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
        if not self.dry_run:
            self.client = pubsub_v1.PublisherClient()

    def publish(self, article: Article) -> None:
        data = article.model_dump_json().encode("utf-8")
        if self.dry_run:
            logger.info("DRY_RUN: would publish article url=%s", article.url)
            return
        self.client.publish(self.topic, data)
