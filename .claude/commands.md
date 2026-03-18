# Common Commands

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
playwright install chromium
```

## Dev Mode (no MongoDB or Pub/Sub required)

```bash
# File-based URL source + console publisher (uses data/input/urls.txt by default)
URL_SOURCE=file MESSAGING_BACKEND=console scrapy crawl article_spider

# Override the URL file
URL_SOURCE=file MESSAGING_BACKEND=console FEED_FILE=data/input/custom.txt scrapy crawl article_spider
```

## Run

```bash
# Run with a URL list file
scrapy crawl article_spider -s FEED_FILE=data/input/urls.txt

# Run with a single URL
scrapy crawl article_spider -a url=https://example.com/article

# Dry run (skip Pub/Sub publish)
DRY_RUN=true scrapy crawl article_spider -s FEED_FILE=data/input/urls.txt
```

## Test

```bash
pytest                                          # all tests
pytest tests/unit/                              # unit only
pytest tests/integration/                       # integration only
pytest --cov=src --cov-report=term-missing      # with coverage
```

## Lint & Format

```bash
ruff check src/ tests/
ruff format src/ tests/
mypy src/
```

## Docker

```bash
docker build -t content-ingestion-agent .

docker run --rm \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -e PUBSUB_TOPIC=projects/my-project/topics/articles \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/credentials.json:/app/credentials.json \
  content-ingestion-agent
```

## Pub/Sub Local Emulator

```bash
gcloud beta emulators pubsub start --project=local-dev
export PUBSUB_EMULATOR_HOST=localhost:8085
```
