from datetime import date as Date, datetime

from pydantic import BaseModel


class Article(BaseModel):
    url: str
    source: str
    title: str
    date: Date | None = None
    author: str | None = None
    text: str
    fetched_at: datetime
    parser_used: str
