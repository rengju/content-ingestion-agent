from datetime import date, datetime

from pydantic import BaseModel


class Article(BaseModel):
    url: str
    source: str
    title: str
    date: date | None = None
    author: str | None = None
    text: str
    fetched_at: datetime
    parser_used: str
