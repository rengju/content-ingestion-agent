FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt pyproject.toml scrapy.cfg ./
COPY src/ ./src/

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium --with-deps

COPY . .

CMD ["scrapy", "crawl", "article_spider"]
