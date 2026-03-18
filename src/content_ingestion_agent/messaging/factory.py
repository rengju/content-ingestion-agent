import os

from content_ingestion_agent.messaging.publisher import Publisher


def get_publisher() -> Publisher:
    backend = os.getenv("MESSAGING_BACKEND", "pubsub")
    if backend == "pubsub":
        from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
        return PubSubPublisher()
    if backend == "console":
        from content_ingestion_agent.messaging.console_publisher import ConsolePublisher
        return ConsolePublisher()
    raise ValueError(f"Unsupported MESSAGING_BACKEND: {backend!r}")
