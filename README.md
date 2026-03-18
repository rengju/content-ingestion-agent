# content-ingestion-agent

A Python-based crawler/parser service that extracts structured article data from websites and publishes it to GCP Pub/Sub for downstream processing.

## Architecture

```
MongoDB (URLs) → Crawler (Scrapy/Playwright) → Parser (Trafilatura) → Pub/Sub
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure environment

```bash
cp configs/.env.example .env
# Edit .env with your values
```

See `configs/.env.example` for all required environment variables.

### 3. Run

```bash
scrapy crawl article_spider
```

Set `DRY_RUN=true` to skip Pub/Sub publishing during local development (articles will be printed to stdout instead).

## Documentation

- `docs/input_schema.md` — MongoDB URL document schema
- `docs/output_schema.md` — Article output schema published to Pub/Sub
- `.claude/CLAUDE.md` — Architecture, conventions, and development guidance
