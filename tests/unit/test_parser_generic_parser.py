from datetime import date, datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from content_ingestion_agent.models.article import Article
from content_ingestion_agent.parser.generic_parser import GenericParser

PATCH_TARGET = "content_ingestion_agent.parser.generic_parser.trafilatura.bare_extraction"

_FIXED_DT = datetime(2026, 3, 17, 20, 30, 0, tzinfo=timezone.utc)
_URL = "https://techcrunch.com/2026/03/17/ai-beats-human"


def _mock_doc(overrides: dict | None = None) -> MagicMock:
    defaults = {
        "title": "Test Title",
        "author": "Jane Smith",
        "text": "Body text.",
        "date": "2026-03-17",
    }
    if overrides:
        defaults.update(overrides)
    return MagicMock(as_dict=MagicMock(return_value=defaults))


def test_can_parse_always_true():
    """can_parse always returns True for any URL and HTML."""
    parser = GenericParser()
    assert parser.can_parse("https://any.com/path", "<html></html>") is True


def test_can_parse_empty_inputs():
    """can_parse returns True even for empty URL and HTML strings."""
    parser = GenericParser()
    assert parser.can_parse("", "") is True


def test_parse_returns_article():
    """parse returns an Article instance."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc()):
        result = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert isinstance(result, Article)


def test_parse_maps_title():
    """Article title is taken from the trafilatura extraction result."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc({"title": "My Title"})):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.title == "My Title"


def test_parse_maps_author():
    """Article author is taken from the trafilatura extraction result."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc({"author": "Jane Smith"})):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.author == "Jane Smith"


def test_parse_maps_text():
    """Article text is taken from the trafilatura extraction result."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc({"text": "Body"})):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.text == "Body"


def test_parse_maps_date_from_iso_string():
    """The date string from trafilatura is converted to a date object."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc({"date": "2026-03-17"})):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.date == date(2026, 3, 17)


def test_parse_date_none_when_missing():
    """Article date is None when trafilatura returns None for date."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc({"date": None})):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.date is None


def test_parse_date_none_when_empty_string():
    """Article date is None when trafilatura returns an empty date string."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc({"date": ""})):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.date is None


def test_parse_source_from_netloc():
    """Article source is derived from the URL's network location."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc()):
        article = parser.parse(url="https://techcrunch.com/path", html="<html/>", fetched_at=_FIXED_DT)
    assert article.source == "techcrunch.com"


def test_parse_url_stored_verbatim():
    """The original URL is stored in the Article without modification."""
    parser = GenericParser()
    url = "https://techcrunch.com/2026/03/17/ai-beats-human?ref=rss"
    with patch(PATCH_TARGET, return_value=_mock_doc()):
        article = parser.parse(url=url, html="<html/>", fetched_at=_FIXED_DT)
    assert article.url == url


def test_parse_fetched_at_passthrough():
    """The fetched_at timestamp is passed through unchanged."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc()):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.fetched_at == _FIXED_DT


def test_parse_parser_used():
    """parser_used is set to 'generic_trafilatura'."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc()):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.parser_used == "generic_trafilatura"


def test_parse_title_defaults_to_empty_string_when_none():
    """Article title defaults to an empty string when trafilatura returns None."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc({"title": None})):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.title == ""


def test_parse_text_defaults_to_empty_string_when_none():
    """Article text defaults to an empty string when trafilatura returns None."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=_mock_doc({"text": None})):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.text == ""


def test_parse_when_trafilatura_returns_none():
    """Article has empty title, text, and no date when trafilatura returns None."""
    parser = GenericParser()
    with patch(PATCH_TARGET, return_value=None):
        article = parser.parse(url=_URL, html="<html/>", fetched_at=_FIXED_DT)
    assert article.title == ""
    assert article.text == ""
    assert article.date is None


def test_parse_calls_bare_extraction_correctly():
    """bare_extraction is called with the correct HTML, URL, and no comments."""
    parser = GenericParser()
    html = "<html><body>content</body></html>"
    with patch(PATCH_TARGET, return_value=_mock_doc()) as mock_extract:
        parser.parse(url=_URL, html=html, fetched_at=_FIXED_DT)
    mock_extract.assert_called_once_with(html, url=_URL, include_comments=False)
