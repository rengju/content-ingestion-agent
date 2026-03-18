import os


class Settings:
    # MongoDB (optional when URL_SOURCE=file)
    mongodb_uri: str = os.getenv("MONGODB_URI", "")
    mongodb_db: str = os.getenv("MONGODB_DB", "")
    mongodb_collection: str = os.getenv("MONGODB_COLLECTION", "")

    # Messaging
    messaging_backend: str = os.getenv("MESSAGING_BACKEND", "pubsub")
    pubsub_topic: str = os.getenv("PUBSUB_TOPIC", "")
    dry_run: bool = os.getenv("DRY_RUN", "false").lower() == "true"

    # URL source
    url_source: str = os.getenv("URL_SOURCE", "mongo")  # "mongo" | "file"
    feed_file: str = os.getenv("FEED_FILE", "data/input/urls.txt")

    # Crawler
    crawl_delay: float = float(os.getenv("CRAWL_DELAY", "1"))
    concurrent_requests: int = int(os.getenv("CONCURRENT_REQUESTS", "8"))
    robotstxt_obey: bool = os.getenv("ROBOTSTXT_OBEY", "true").lower() == "true"
    user_agent: str = os.getenv("USER_AGENT", "content-ingestion-agent/1.0")


settings = Settings()
