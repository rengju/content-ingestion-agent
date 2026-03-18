# Conventions

## 1. Separation of Concerns

- crawler → discovery + fetch
- parser → extraction + normalization
- messaging → publish

Never mix responsibilities.

---

## 2. Parsing Strategy

Always follow:

1. Trafilatura (default)
2. BeautifulSoup fallback
3. Site plugin (only if needed)

Do not write site-specific logic first.

---

## 3. Data Contract

- All outputs must follow Article schema
- Use pydantic validation
- No raw/unstructured data beyond parser

---

## 4. Messaging First

- Parser must publish to messaging
- No direct calls to consumer/output
- All downstream reads from messages

---

## 5. Output Rules

- Default format: JSON
- One article per line
- File writing only in consumer layer

---

## 6. Extensibility

- Add new sites via parser/plugins/
- Keep plugins minimal
- Do not modify core parser unless global benefit

---

## 7. Performance

- Prefer HTTP over Playwright
- Use browser only when necessary
- Deduplicate before fetch

---

## 8. Testing

- Use saved HTML fixtures
- Do not rely on live crawling

---

## 9. General Rules

- Keep modules small and focused
- Prefer composition over inheritance
- Avoid tight coupling