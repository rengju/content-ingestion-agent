from content_ingestion_agent.common.settings import settings
from content_ingestion_agent.crawler.url_source import UrlSource


def get_url_source() -> UrlSource:
    if settings.url_source == "file":
        from content_ingestion_agent.crawler.file_url_source import FileUrlSource
        return FileUrlSource(settings.feed_file)
    if settings.url_source == "mongo":
        from content_ingestion_agent.crawler.mongo_url_source import MongoUrlSource
        return MongoUrlSource(
            uri=settings.mongodb_uri,
            db=settings.mongodb_db,
            collection=settings.mongodb_collection,
        )
    raise ValueError(f"Unknown url_source: {settings.url_source!r}")
