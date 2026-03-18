# MongoDB Input Schema

Each document in the URL collection represents a single article URL to be crawled.

## Document Structure

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | `string` | required | The article URL to crawl |
| `status` | `string` | `pending` | Crawl status: `pending`, `done`, `failed` |
| `crawled_at` | `datetime` | `null` | Timestamp when last crawled |
| `error` | `string` | `null` | Error message if status is `failed` |
| `priority` | `integer` | `0` | Crawl priority — higher value = higher priority |
| `retry_count` | `integer` | `0` | Number of retry attempts |
| `domain` | `string` | derived from `url` | Domain extracted from URL on insert |

## Example Document

```json
{
  "url": "https://techcrunch.com/2024/01/01/example-article",
  "status": "pending",
  "crawled_at": null,
  "error": null,
  "priority": 0,
  "retry_count": 0,
  "domain": "techcrunch.com"
}
```
