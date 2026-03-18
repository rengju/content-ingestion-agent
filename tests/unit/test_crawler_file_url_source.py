import pytest

from content_ingestion_agent.crawler.file_url_source import FileUrlSource
from content_ingestion_agent.models.url_item import CrawlStatus, UrlItem


def _write(tmp_path, content: str) -> str:
    f = tmp_path / "urls.txt"
    f.write_text(content)
    return str(f)


def test_pending_urls_yields_valid_urls(tmp_path):
    """All valid URLs in the file are yielded as UrlItems."""
    path = _write(tmp_path, "https://a.com\nhttps://b.com\nhttps://c.com\n")
    source = FileUrlSource(path)
    urls = [item.url for item in source.pending_urls()]
    assert urls == ["https://a.com", "https://b.com", "https://c.com"]


def test_pending_urls_skips_blank_lines(tmp_path):
    """Blank lines in the URL file are silently ignored."""
    path = _write(tmp_path, "https://a.com\n\nhttps://b.com\n")
    source = FileUrlSource(path)
    urls = [item.url for item in source.pending_urls()]
    assert urls == ["https://a.com", "https://b.com"]


def test_pending_urls_skips_comment_lines(tmp_path):
    """Lines starting with # are treated as comments and skipped."""
    path = _write(tmp_path, "# comment\nhttps://a.com\n# another\nhttps://b.com\n")
    source = FileUrlSource(path)
    urls = [item.url for item in source.pending_urls()]
    assert urls == ["https://a.com", "https://b.com"]


def test_pending_urls_empty_file_yields_nothing(tmp_path):
    """An empty file produces no UrlItems."""
    path = _write(tmp_path, "")
    source = FileUrlSource(path)
    assert list(source.pending_urls()) == []


def test_pending_urls_strips_whitespace(tmp_path):
    """Leading and trailing whitespace is stripped from each URL."""
    path = _write(tmp_path, "  https://a.com  \n  https://b.com\n")
    source = FileUrlSource(path)
    urls = [item.url for item in source.pending_urls()]
    assert urls == ["https://a.com", "https://b.com"]


def test_pending_urls_yields_url_items(tmp_path):
    """Each yielded item is a UrlItem instance."""
    path = _write(tmp_path, "https://a.com\n")
    source = FileUrlSource(path)
    items = list(source.pending_urls())
    assert all(isinstance(item, UrlItem) for item in items)


def test_pending_urls_items_have_pending_status(tmp_path):
    """All yielded UrlItems have PENDING status."""
    path = _write(tmp_path, "https://a.com\nhttps://b.com\n")
    source = FileUrlSource(path)
    items = list(source.pending_urls())
    assert all(item.status == CrawlStatus.PENDING for item in items)


def test_mark_done_is_noop(tmp_path):
    """mark_done does nothing and leaves the file unchanged."""
    f = tmp_path / "urls.txt"
    f.write_text("https://a.com\n")
    source = FileUrlSource(str(f))
    source.mark_done("https://a.com")  # should not raise
    assert f.read_text() == "https://a.com\n"  # file unchanged


def test_mark_failed_is_noop(tmp_path):
    """mark_failed does nothing and does not raise."""
    path = _write(tmp_path, "https://a.com\n")
    source = FileUrlSource(path)
    source.mark_failed("https://a.com", "timeout")  # should not raise


def test_file_not_found_raises(tmp_path):
    """FileNotFoundError is raised when the path does not exist."""
    source = FileUrlSource(str(tmp_path / "nonexistent.txt"))
    with pytest.raises(FileNotFoundError):
        list(source.pending_urls())
