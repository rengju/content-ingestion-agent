# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An AI-agent-driven application development project that includes a Python-based crawler/parser service to extract structured website article data and publish it to Pub/Sub for downstream processing.

## Architecture

**MongoDB** (URL input source)

↓

**Crawler** (Read URLs from MongoDB)

↓

**Parser** (Parse HTML, extract content → Article schema)

↓

**Pub/Sub** (event streaming)

## Tech Stack

- **Python 3.12**
- **MongoDB** Input source for URLs to crawl
- **Scrapy** A full crawling framework
- **Playwright** A headless browser
- **scrapy-playwright** Glue between Scrapy and Playwright
- **Trafilatura** An AI-style content extractor
- **Beautiful Soup** A DOM parser
- **lxml** Fast parsing engine
- **Pydantic** Schema + validation
- **GCP Pub/Sub** Message bus for publishing crawl results

## Project Structure

```
content-ingestion-agent/
├── .claude/
│   ├── agents/
│   ├── commands/
│   ├── skills/
│   │   ├── architecture/
│   │   ├── crawler/
│   │   ├── parser/
│   │   ├── messaging/
│   │   └── troubleshooting/
│   └── memory/
├── configs/
├── data/
│   └── input/
├── docs/
├── src/
│   └── content_ingestion_agent/
│       ├── common/
│       ├── models/
│       ├── crawler/
│       │   └── spiders/
│       ├── parser/
│       │   └── plugins/
│       └── messaging/
├── tests/
│   ├── fixtures/
│   │   ├── html/
│   │   └── messages/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
├── docker/
└── deploy/
    └── gcp/
```

## Configuration

### App

| Env Var | Description |
|---------|-------------|
| `MESSAGING_BACKEND` | Message bus backend: `pubsub` (default), future: `sqs`, `azure_servicebus` |
| `MONGODB_URI` | Full MongoDB connection string (includes credentials) |
| `MONGODB_DB` | Database name |
| `MONGODB_COLLECTION` | Collection containing URLs to crawl |
| `PUBSUB_TOPIC` | Full Pub/Sub topic path (`projects/<project>/topics/<topic>`) |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account key file |
| `DRY_RUN` | Skip Pub/Sub publish when `true` (local dev) |

### Crawler

| Env Var | Description |
|---------|-------------|
| `CRAWL_DELAY` | Seconds between requests (default: `1`) |
| `CONCURRENT_REQUESTS` | Parallel requests Scrapy makes (default: `8`) |
| `ROBOTSTXT_OBEY` | Enforce robots.txt — `true` or `false` (default: `true`) |
| `USER_AGENT` | Crawler identity string sent with each request |

## Conventions

- crawler reads URLs from MongoDB (see [input_schema.md](../docs/input_schema.md))
- crawler = discovery/fetch only
- parser = extraction + normalization only
- service output = publish to messaging as final step
- publish one Article JSON message per parsed article
- do not batch before publishing
- no file writing or storage logic in this service
- use generic parser first (Trafilatura), plugins only if needed
- all outputs must follow Article schema (see [output_schema.md](../docs/output_schema.md))
- Playwright only when necessary
- Print output message console if message bus is mocked

## Common Commands

See [commands.md](commands.md) for all common commands.

## Security Notes

- Do not log sensitive data (tokens, credentials, cookies)
- Do not hardcode secrets (use env/config)
- Respect robots.txt and site terms where applicable
- Avoid aggressive crawling (rate limit requests)

## Testing Rules
- Write tests BEFORE implementation (TDD) when asked to add features
- After writing a function, switch mindset: how would this break?
- Test the contract (inputs/outputs) not the implementation details
- If you wrote the code, explicitly look for edge cases you assumed away