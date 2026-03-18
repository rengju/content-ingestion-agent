import json
from unittest.mock import patch

import pytest

from content_ingestion_agent.messaging.console_publisher import ConsolePublisher
from content_ingestion_agent.models.article import Article

PATCH_TARGET = "content_ingestion_agent.messaging.console_publisher.logger"


def test_publish_calls_logger_info(sample_article):
    """publish logs exactly one info-level message."""
    publisher = ConsolePublisher()
    with patch(PATCH_TARGET) as mock_logger:
        publisher.publish(sample_article)
    mock_logger.info.assert_called_once()


def test_publish_log_format_string(sample_article):
    """The log format string matches the expected [CONSOLE PUBLISHER] prefix."""
    publisher = ConsolePublisher()
    with patch(PATCH_TARGET) as mock_logger:
        publisher.publish(sample_article)
    args = mock_logger.info.call_args[0]
    assert args[0] == "[CONSOLE PUBLISHER] %s"


def test_publish_log_second_arg_is_json(sample_article):
    """The second log argument is valid JSON."""
    publisher = ConsolePublisher()
    with patch(PATCH_TARGET) as mock_logger:
        publisher.publish(sample_article)
    json_arg = mock_logger.info.call_args[0][1]
    parsed = json.loads(json_arg)
    assert isinstance(parsed, dict)


def test_publish_json_contains_url(sample_article):
    """The logged JSON includes the article's URL."""
    publisher = ConsolePublisher()
    with patch(PATCH_TARGET) as mock_logger:
        publisher.publish(sample_article)
    json_arg = mock_logger.info.call_args[0][1]
    assert sample_article.url in json_arg


def test_publish_json_validates_as_article(sample_article):
    """The logged JSON deserialises back to an identical Article."""
    publisher = ConsolePublisher()
    with patch(PATCH_TARGET) as mock_logger:
        publisher.publish(sample_article)
    json_arg = mock_logger.info.call_args[0][1]
    restored = Article.model_validate_json(json_arg)
    assert restored == sample_article


def test_publish_returns_none(sample_article):
    """publish has no return value."""
    publisher = ConsolePublisher()
    with patch(PATCH_TARGET):
        result = publisher.publish(sample_article)
    assert result is None
