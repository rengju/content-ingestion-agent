import json
from unittest.mock import MagicMock, patch

import pytest

PATCH_CLIENT = "content_ingestion_agent.messaging.pubsub_publisher.pubsub_v1.PublisherClient"
PATCH_LOGGER = "content_ingestion_agent.messaging.pubsub_publisher.logger"


def _make_publisher(monkeypatch, topic="projects/p/topics/t", dry_run=None):
    monkeypatch.setenv("PUBSUB_TOPIC", topic)
    if dry_run is not None:
        monkeypatch.setenv("DRY_RUN", dry_run)
    else:
        monkeypatch.delenv("DRY_RUN", raising=False)
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with patch(PATCH_CLIENT) as mock_client_cls:
        publisher = PubSubPublisher()
    return publisher, mock_client_cls


def test_init_reads_pubsub_topic(monkeypatch):
    """The topic attribute is set from the PUBSUB_TOPIC env var."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.delenv("DRY_RUN", raising=False)
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with patch(PATCH_CLIENT):
        publisher = PubSubPublisher()
    assert publisher.topic == "projects/p/topics/t"


def test_init_raises_if_topic_missing(monkeypatch):
    """KeyError is raised when PUBSUB_TOPIC is not set."""
    monkeypatch.delenv("PUBSUB_TOPIC", raising=False)
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with pytest.raises(KeyError):
        PubSubPublisher()


def test_init_creates_client_in_live_mode(monkeypatch):
    """PublisherClient is created when DRY_RUN is false."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.setenv("DRY_RUN", "false")
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with patch(PATCH_CLIENT) as mock_client_cls:
        PubSubPublisher()
    mock_client_cls.assert_called_once()


def test_init_no_client_in_dry_run(monkeypatch):
    """PublisherClient is not created when DRY_RUN is true."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.setenv("DRY_RUN", "true")
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with patch(PATCH_CLIENT) as mock_client_cls:
        PubSubPublisher()
    mock_client_cls.assert_not_called()


def test_dry_run_true_from_env(monkeypatch):
    """dry_run attribute is True when DRY_RUN env var is 'true'."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.setenv("DRY_RUN", "true")
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    publisher = PubSubPublisher()
    assert publisher.dry_run is True


def test_dry_run_false_when_missing(monkeypatch):
    """dry_run attribute is False when DRY_RUN env var is absent."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.delenv("DRY_RUN", raising=False)
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with patch(PATCH_CLIENT):
        publisher = PubSubPublisher()
    assert publisher.dry_run is False


def test_publish_dry_run_does_not_call_client(monkeypatch, sample_article):
    """publish skips the Pub/Sub client call in dry-run mode."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.setenv("DRY_RUN", "true")
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    publisher = PubSubPublisher()
    mock_client = MagicMock()
    publisher.client = mock_client  # should not be called
    with patch(PATCH_LOGGER):
        publisher.publish(sample_article)
    mock_client.publish.assert_not_called()


def test_publish_dry_run_logs(monkeypatch, sample_article):
    """publish logs a DRY_RUN message instead of calling the client."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.setenv("DRY_RUN", "true")
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    publisher = PubSubPublisher()
    with patch(PATCH_LOGGER) as mock_logger:
        publisher.publish(sample_article)
    mock_logger.info.assert_called_once()
    log_msg = mock_logger.info.call_args[0][0]
    assert "DRY_RUN" in log_msg


def test_publish_live_calls_client_publish(monkeypatch, sample_article):
    """publish calls the Pub/Sub client exactly once in live mode."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.setenv("DRY_RUN", "false")
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with patch(PATCH_CLIENT) as mock_client_cls:
        mock_client_instance = MagicMock()
        mock_client_cls.return_value = mock_client_instance
        publisher = PubSubPublisher()
    publisher.publish(sample_article)
    mock_client_instance.publish.assert_called_once()


def test_publish_live_uses_correct_topic(monkeypatch, sample_article):
    """publish passes the configured topic as the first argument to the client."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.setenv("DRY_RUN", "false")
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with patch(PATCH_CLIENT) as mock_client_cls:
        mock_client_instance = MagicMock()
        mock_client_cls.return_value = mock_client_instance
        publisher = PubSubPublisher()
    publisher.publish(sample_article)
    call_args = mock_client_instance.publish.call_args[0]
    assert call_args[0] == "projects/p/topics/t"


def test_publish_live_data_is_utf8_json(monkeypatch, sample_article):
    """The message payload is UTF-8 encoded JSON bytes."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.setenv("DRY_RUN", "false")
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    with patch(PATCH_CLIENT) as mock_client_cls:
        mock_client_instance = MagicMock()
        mock_client_cls.return_value = mock_client_instance
        publisher = PubSubPublisher()
    publisher.publish(sample_article)
    data = mock_client_instance.publish.call_args[0][1]
    assert isinstance(data, bytes)
    parsed = json.loads(data.decode("utf-8"))
    assert isinstance(parsed, dict)


def test_publish_live_data_round_trips_to_article(monkeypatch, sample_article):
    """The payload deserialises back to an identical Article."""
    monkeypatch.setenv("PUBSUB_TOPIC", "projects/p/topics/t")
    monkeypatch.setenv("DRY_RUN", "false")
    from content_ingestion_agent.messaging.pubsub_publisher import PubSubPublisher
    from content_ingestion_agent.models.article import Article
    with patch(PATCH_CLIENT) as mock_client_cls:
        mock_client_instance = MagicMock()
        mock_client_cls.return_value = mock_client_instance
        publisher = PubSubPublisher()
    publisher.publish(sample_article)
    data = mock_client_instance.publish.call_args[0][1]
    restored = Article.model_validate_json(data.decode("utf-8"))
    assert restored == sample_article
