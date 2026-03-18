from content_ingestion_agent.common.settings import settings

BOT_NAME = "content-ingestion-agent"

SPIDER_MODULES = ["content_ingestion_agent.crawler.spiders"]
NEWSPIDER_MODULE = "content_ingestion_agent.crawler.spiders"

ROBOTSTXT_OBEY = settings.robotstxt_obey
CONCURRENT_REQUESTS = settings.concurrent_requests
DOWNLOAD_DELAY = settings.crawl_delay
USER_AGENT = settings.user_agent

# Disable default logging for scrapy internals (keep app logs readable)
LOG_LEVEL = "INFO"
