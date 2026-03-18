from unittest.mock import MagicMock, patch

import pytest
import scrapy

from content_ingestion_agent.models.url_item import UrlItem

GET_URL_SOURCE = "content_ingestion_agent.crawler.spiders.article_spider.get_url_source"
GENERIC_PARSER = "content_ingestion_agent.crawler.spiders.article_spider.GenericParser"
GET_PUBLISHER = "content_ingestion_agent.crawler.spiders.article_spider.get_publisher"


def _make_url_items(*urls):
    return [UrlItem(url=u) for u in urls]


@pytest.fixture
def spider_file():
    """ArticleSpider with all collaborators mocked."""
    mock_url_source_instance = MagicMock()
    mock_parser_instance = MagicMock()
    mock_publisher_instance = MagicMock()

    with patch(GET_URL_SOURCE, return_value=mock_url_source_instance), \
         patch(GENERIC_PARSER, return_value=mock_parser_instance), \
         patch(GET_PUBLISHER, return_value=mock_publisher_instance):
        from content_ingestion_agent.crawler.spiders.article_spider import ArticleSpider
        spider = ArticleSpider()

    return spider, mock_url_source_instance, mock_parser_instance, mock_publisher_instance


# --- init tests ---

def test_init_calls_get_url_source():
    """get_url_source is called during spider initialisation."""
    with patch(GET_URL_SOURCE) as mock_get_source, \
         patch(GENERIC_PARSER), \
         patch(GET_PUBLISHER):
        from content_ingestion_agent.crawler.spiders.article_spider import ArticleSpider
        ArticleSpider()
    mock_get_source.assert_called_once()


def test_init_creates_generic_parser():
    """GenericParser is created during spider initialisation."""
    with patch(GET_URL_SOURCE), \
         patch(GENERIC_PARSER) as mock_parser_cls, \
         patch(GET_PUBLISHER):
        from content_ingestion_agent.crawler.spiders.article_spider import ArticleSpider
        ArticleSpider()
    mock_parser_cls.assert_called_once()


def test_init_calls_get_publisher():
    """get_publisher is called during spider initialisation."""
    with patch(GET_URL_SOURCE), \
         patch(GENERIC_PARSER), \
         patch(GET_PUBLISHER) as mock_get_pub:
        from content_ingestion_agent.crawler.spiders.article_spider import ArticleSpider
        ArticleSpider()
    mock_get_pub.assert_called_once()


# --- start_requests tests ---

def test_start_requests_yields_one_request_per_url(spider_file):
    """One Scrapy Request is yielded for each pending URL."""
    spider, mock_url_source, _, _ = spider_file
    items = _make_url_items("https://a.com", "https://b.com", "https://c.com")
    mock_url_source.pending_urls.return_value = iter(items)
    requests = list(spider.start_requests())
    assert len(requests) == 3


def test_start_requests_request_url(spider_file):
    """Each yielded Request targets the URL from the URL source."""
    spider, mock_url_source, _, _ = spider_file
    items = _make_url_items("https://a.com", "https://b.com")
    mock_url_source.pending_urls.return_value = iter(items)
    requests = list(spider.start_requests())
    assert requests[0].url == "https://a.com"
    assert requests[1].url == "https://b.com"


def test_start_requests_callback_is_parse(spider_file):
    """Callback is None (Scrapy default), meaning spider.parse will be called."""
    spider, mock_url_source, _, _ = spider_file
    mock_url_source.pending_urls.return_value = iter(_make_url_items("https://a.com"))
    requests = list(spider.start_requests())
    assert requests[0].callback is None


def test_start_requests_errback_is_errback(spider_file):
    """Each Request's errback is set to the spider's errback method."""
    spider, mock_url_source, _, _ = spider_file
    mock_url_source.pending_urls.return_value = iter(_make_url_items("https://a.com"))
    requests = list(spider.start_requests())
    assert requests[0].errback == spider.errback


def test_start_requests_cb_kwargs_contains_url(spider_file):
    """cb_kwargs carries the original URL string for use inside parse."""
    spider, mock_url_source, _, _ = spider_file
    mock_url_source.pending_urls.return_value = iter(_make_url_items("https://a.com"))
    requests = list(spider.start_requests())
    assert requests[0].cb_kwargs == {"url": "https://a.com"}


# --- parse tests ---

def test_parse_calls_parser_with_html(spider_file, sample_article):
    """parse passes the response body HTML to the parser."""
    spider, _, mock_parser, _ = spider_file
    mock_parser.parse.return_value = sample_article
    response = MagicMock()
    response.text = "<html>content</html>"
    spider.parse(response, url="https://a.com")
    call_kwargs = mock_parser.parse.call_args[1]
    assert call_kwargs["html"] == "<html>content</html>"


def test_parse_calls_parser_with_url(spider_file, sample_article):
    """parse passes the request URL to the parser."""
    spider, _, mock_parser, _ = spider_file
    mock_parser.parse.return_value = sample_article
    response = MagicMock()
    response.text = "<html/>"
    spider.parse(response, url="https://techcrunch.com/article")
    call_kwargs = mock_parser.parse.call_args[1]
    assert call_kwargs["url"] == "https://techcrunch.com/article"


def test_parse_calls_publisher(spider_file, sample_article):
    """parse publishes the resulting Article via the publisher."""
    spider, mock_url_source, mock_parser, mock_publisher = spider_file
    mock_parser.parse.return_value = sample_article
    response = MagicMock()
    response.text = "<html/>"
    spider.parse(response, url="https://a.com")
    mock_publisher.publish.assert_called_once_with(sample_article)


def test_parse_calls_mark_done(spider_file, sample_article):
    """parse marks the URL as done in the URL source after success."""
    spider, mock_url_source, mock_parser, _ = spider_file
    mock_parser.parse.return_value = sample_article
    response = MagicMock()
    response.text = "<html/>"
    spider.parse(response, url="https://a.com")
    mock_url_source.mark_done.assert_called_once_with("https://a.com")


# --- errback tests ---

def test_errback_calls_mark_failed(spider_file):
    """errback marks the URL as failed when a request error occurs."""
    spider, mock_url_source, _, _ = spider_file
    failure = MagicMock()
    failure.request.url = "https://a.com"
    failure.value = Exception("timeout")
    spider.errback(failure)
    mock_url_source.mark_failed.assert_called_once()
    call_kwargs = mock_url_source.mark_failed.call_args[1]
    assert call_kwargs["url"] == "https://a.com"


def test_errback_passes_error_repr(spider_file):
    """errback records the repr of the exception as the error message."""
    spider, mock_url_source, _, _ = spider_file
    exc = Exception("connection refused")
    failure = MagicMock()
    failure.request.url = "https://a.com"
    failure.value = exc
    spider.errback(failure)
    call_kwargs = mock_url_source.mark_failed.call_args[1]
    assert call_kwargs["error"] == repr(exc)


def test_errback_does_not_raise(spider_file):
    spider, _, _, _ = spider_file
    failure = MagicMock()
    failure.request.url = "https://a.com"
    failure.value = Exception("boom")
    spider.errback(failure)  # must not raise
