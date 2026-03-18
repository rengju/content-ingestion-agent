import pytest
from unittest.mock import patch

PATCH_CLIENT = "content_ingestion_agent.messaging.pubsub_publisher.pubsub_v1.PublisherClient"


def test_returns_pubsub_publisher_by_default(monkeypatch):
    """PubSubPublisher is returned when MESSAGING_BACKEND is not set."""
    monkeypatch.delenv("MESSAGING_BACKEND", raising=False)
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.delenv("DRY_RUN", raising=False)
    from content_ingestion_agent.messaging.factory import get_publisher
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with patch(PATCH_CLIENT):
        publisher = get_publisher()
    assert isinstance(publisher, PubSubPublisher)


def test_returns_pubsub_publisher_explicit(monkeypatch):
    """PubSubPublisher is returned when MESSAGING_BACKEND is set to 'pubsub'."""
    monkeypatch.setenv("MESSAGING_BACKEND", "pubsub")
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.delenv("DRY_RUN", raising=False)
    from content_ingestion_agent.messaging.factory import get_publisher
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with patch(PATCH_CLIENT):
        publisher = get_publisher()
    assert isinstance(publisher, PubSubPublisher)


def test_returns_console_publisher(monkeypatch):
    """ConsolePublisher is returned when MESSAGING_BACKEND is 'console'."""
    monkeypatch.setenv("MESSAGING_BACKEND", "console")
    from content_ingestion_agent.messaging.factory import get_publisher
    from content_ingestion_agent.messaging.console_publisher import ConsolePublisher
    publisher = get_publisher()
    assert isinstance(publisher, ConsolePublisher)


def test_raises_for_unknown_backend(monkeypatch):
    """ValueError is raised for an unrecognised backend name."""
    monkeypatch.setenv("MESSAGING_BACKEND", "kafka")
    from content_ingestion_agent.messaging.factory import get_publisher
    with pytest.raises(ValueError):
        get_publisher()


def test_error_message_contains_backend_name(monkeypatch):
    """The ValueError message includes the unknown backend name."""
    monkeypatch.setenv("MESSAGING_BACKEND", "sqs")
    from content_ingestion_agent.messaging.factory import get_publisher
    with pytest.raises(ValueError, match="sqs"):
        get_publisher()
