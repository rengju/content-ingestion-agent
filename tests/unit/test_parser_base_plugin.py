"""TDD tests for BasePlugin.can_parse — drives implementation of the stub."""
import pytest

from content_ingestion_agent.models.article import Article
from content_ingestion_agent.parser.plugins.base_plugin import BasePlugin


class TechCrunchPlugin(BasePlugin):
    @property
    def domain(self) -> str:
        return "techcrunch.com"

    def parse(self, url, html, fetched_at) -> Article:
        raise NotImplementedError


def test_can_parse_true_for_matching_domain():
    """can_parse returns True when the URL's domain matches the plugin domain."""
    plugin = TechCrunchPlugin()
    assert plugin.can_parse("https://techcrunch.com/article", "") is True


def test_can_parse_false_for_different_domain():
    """can_parse returns False when the URL's domain does not match."""
    plugin = TechCrunchPlugin()
    assert plugin.can_parse("https://bbc.com/article", "") is False


def test_can_parse_false_for_subdomain():
    """can_parse returns False for subdomains of the plugin domain."""
    plugin = TechCrunchPlugin()
    assert plugin.can_parse("https://sub.techcrunch.com/x", "") is False


def test_can_parse_html_arg_ignored():
    """can_parse result is based solely on the URL, not the HTML content."""
    plugin = TechCrunchPlugin()
    assert plugin.can_parse("https://techcrunch.com/x", "<html>anything</html>") is True
    assert plugin.can_parse("https://bbc.com/x", "<html>techcrunch.com</html>") is False


def test_cannot_instantiate_without_domain():
    """TypeError is raised when a subclass does not implement the domain property."""
    class NoDomain(BasePlugin):
        def parse(self, url, html, fetched_at) -> Article:
            raise NotImplementedError

    with pytest.raises(TypeError):
        Noomain = NoDomain()  # noqa: F841


def test_cannot_instantiate_without_parse():
    """TypeError is raised when a subclass does not implement the parse method."""
    class NoParse(BasePlugin):
        @property
        def domain(self) -> str:
            return "example.com"

    with pytest.raises(TypeError):
        NoParse()
