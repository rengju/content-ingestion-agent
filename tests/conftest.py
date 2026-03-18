from datetime import date, datetime, timezone

import pytest
from pathlib import Path

from content_ingestion_agent.models.article import Article


@pytest.fixture
def fixed_datetime() -> datetime:
    return datetime(2026, 3, 17, 20, 30, 0, tzinfo=timezone.utc)


@pytest.fixture
def sample_article(fixed_datetime) -> Article:
    return Article(
        url="https://techcrunch.com/2026/03/17/ai-beats-human",
        source="techcrunch.com",
        title="AI Beats Human At Chess Again",
        date=date(2026, 3, 17),
        author="Jane Smith",
        text="A new AI system has defeated the world chess champion.",
        fetched_at=fixed_datetime,
        parser_used="generic_trafilatura",
    )


@pytest.fixture
def html_full() -> str:
    path = Path(__file__).parent / "fixtures/html/article_full.html"
    return path.read_text()


@pytest.fixture
def html_minimal() -> str:
    path = Path(__file__).parent / "fixtures/html/article_minimal.html"
    return path.read_text()
