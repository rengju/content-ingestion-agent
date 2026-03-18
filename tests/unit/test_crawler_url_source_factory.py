import pytest
from unittest.mock import patch, MagicMock

from content_ingestion_agent.common.settings import settings

PATCH_FILE_SOURCE = "content_ingestion_agent.crawler.file_url_source.FileUrlSource"
PATCH_MONGO_SOURCE = "content_ingestion_agent.crawler.mongo_url_source.MongoUrlSource"


def test_get_url_source_file_returns_file_source(monkeypatch):
    """FileUrlSource is returned when url_source setting is 'file'."""
    monkeypatch.setattr(settings, "url_source", "file")
    monkeypatch.setattr(settings, "feed_file", "data/input/urls.txt")
    from content_ingestion_agent.crawler.url_source_factory import get_url_source
    with patch(PATCH_FILE_SOURCE) as mock_cls:
        source = get_url_source()
    assert source is mock_cls.return_value


def test_get_url_source_mongo_returns_mongo_source(monkeypatch):
    """MongoUrlSource is returned when url_source setting is 'mongo'."""
    monkeypatch.setattr(settings, "url_source", "mongo")
    monkeypatch.setattr(settings, "mongodb_uri", "mongodb://localhost/test")
    monkeypatch.setattr(settings, "mongodb_db", "testdb")
    monkeypatch.setattr(settings, "mongodb_collection", "urls")
    from content_ingestion_agent.crawler.url_source_factory import get_url_source
    from content_ingestion_agent.crawler.mongo_url_source import MongoUrlSource
    with patch(PATCH_MONGO_SOURCE) as mock_cls:
        mock_cls.return_value = MagicMock(spec=MongoUrlSource)
        source = get_url_source()
    assert source is mock_cls.return_value


def test_get_url_source_passes_feed_file(monkeypatch):
    """FileUrlSource receives the configured feed_file path."""
    monkeypatch.setattr(settings, "url_source", "file")
    monkeypatch.setattr(settings, "feed_file", "custom/path.txt")
    from content_ingestion_agent.crawler.url_source_factory import get_url_source
    with patch(PATCH_FILE_SOURCE) as mock_cls:
        get_url_source()
    mock_cls.assert_called_once_with("custom/path.txt")


def test_get_url_source_passes_mongo_config(monkeypatch):
    """MongoUrlSource receives uri, db, and collection from settings."""
    monkeypatch.setattr(settings, "url_source", "mongo")
    monkeypatch.setattr(settings, "mongodb_uri", "mongodb://host:27017")
    monkeypatch.setattr(settings, "mongodb_db", "mydb")
    monkeypatch.setattr(settings, "mongodb_collection", "mycol")
    from content_ingestion_agent.crawler.url_source_factory import get_url_source
    with patch(PATCH_MONGO_SOURCE) as mock_cls:
        get_url_source()
    mock_cls.assert_called_once_with(
        uri="mongodb://host:27017",
        db="mydb",
        collection="mycol",
    )


def test_get_url_source_unknown_raises(monkeypatch):
    """ValueError is raised for an unrecognised url_source value."""
    monkeypatch.setattr(settings, "url_source", "s3")
    from content_ingestion_agent.crawler.url_source_factory import get_url_source
    with pytest.raises(ValueError, match="s3"):
        get_url_source()
