from django.db import models
from ninja import Schema


class QuerySchema(Schema):
    query: str


class ResultSchema(Schema):
    origin_url: str
    title: str
    author: list[str]
    organization: list[str] | None = None
    magazine: list[str] | None = None
    publisher: str | None = None
    publication_year: int | None = None
    category: list[str] | None = None
    research_area: str | None = None
    issue_description: str | None = None
    pmid: str | None = None
    doi: str | None = None
    arxiv: str | None = None
    summary: str | None = None
