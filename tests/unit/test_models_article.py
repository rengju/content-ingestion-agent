import json
from datetime import date, datetime, timezone

import pytest
from pydantic import ValidationError

from content_ingestion_agent.models.article import Article


@pytest.fixture
def base_kwargs():
    return dict(
        url="https://example.com/article",
        source="example.com",
        title="Test Title",
        text="Body text.",
        fetched_at=datetime(2026, 3, 17, 20, 30, 0, tzinfo=timezone.utc),
        parser_used="generic_trafilatura",
    )


def test_creation_all_fields(base_kwargs):
    """Article accepts and stores all supported fields correctly."""
    article = Article(
        **base_kwargs,
        date=date(2026, 3, 17),
        author="Jane Smith",
    )
    assert article.url == "https://example.com/article"
    assert article.source == "example.com"
    assert article.title == "Test Title"
    assert article.text == "Body text."
    assert article.date == date(2026, 3, 17)
    assert article.author == "Jane Smith"
    assert article.fetched_at == datetime(2026, 3, 17, 20, 30, 0, tzinfo=timezone.utc)
    assert article.parser_used == "generic_trafilatura"


def test_optional_fields_default_to_none(base_kwargs):
    """Optional fields date and author default to None when omitted."""
    article = Article(**base_kwargs)
    assert article.date is None
    assert article.author is None


def test_date_field_is_date_type(base_kwargs):
    """The date field stores a date object, not a string or datetime."""
    article = Article(**base_kwargs, date=date(2026, 3, 17))
    assert type(article.date) is date


def test_rejects_missing_url(base_kwargs):
    """ValidationError is raised when url is absent."""
    del base_kwargs["url"]
    with pytest.raises(ValidationError):
        Article(**base_kwargs)


def test_rejects_missing_text(base_kwargs):
    """ValidationError is raised when text is absent."""
    del base_kwargs["text"]
    with pytest.raises(ValidationError):
        Article(**base_kwargs)


def test_rejects_missing_title(base_kwargs):
    """ValidationError is raised when title is absent."""
    del base_kwargs["title"]
    with pytest.raises(ValidationError):
        Article(**base_kwargs)


def test_rejects_missing_fetched_at(base_kwargs):
    """ValidationError is raised when fetched_at is absent."""
    del base_kwargs["fetched_at"]
    with pytest.raises(ValidationError):
        Article(**base_kwargs)


def test_model_dump_json_is_valid_json(base_kwargs):
    """model_dump_json produces valid JSON."""
    article = Article(**base_kwargs)
    parsed = json.loads(article.model_dump_json())
    assert isinstance(parsed, dict)


def test_model_dump_json_date_format(base_kwargs):
    """The date field is serialised as an ISO-8601 string."""
    article = Article(**base_kwargs, date=date(2026, 3, 17))
    data = json.loads(article.model_dump_json())
    assert data["date"] == "2026-03-17"


def test_round_trip_via_model_validate_json(base_kwargs):
    """An Article survives a JSON round-trip unchanged."""
    original = Article(**base_kwargs, date=date(2026, 3, 17), author="Jane Smith")
    json_str = original.model_dump_json()
    restored = Article.model_validate_json(json_str)
    assert restored == original
