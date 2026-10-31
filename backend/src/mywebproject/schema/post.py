from __future__ import annotations

from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class ParagraphBlock(BaseModel):
    type: Literal["paragraph"]
    text: str


class HeadingBlock(BaseModel):
    type: Literal["heading"]
    level: int = Field(default=2, ge=1, le=6)
    text: str


class QuoteBlock(BaseModel):
    type: Literal["quote"]
    text: str


class CodeBlock(BaseModel):
    type: Literal["code"]
    lang: str = ""
    code: str


class ListBlock(BaseModel):
    type: Literal["list"]
    ordered: bool = False
    items: list[str]


ContentBlock = Annotated[
    ParagraphBlock | HeadingBlock | QuoteBlock | CodeBlock | ListBlock,
    Field(discriminator="type"),
]


class PostSummary(BaseModel):
    slug: str
    title: str
    summary: str
    date: date
    tags: list[str]
    reading_time: int


class PostDetail(PostSummary):
    content: list[ContentBlock]


class PostListResponse(BaseModel):
    items: list[PostSummary]
    total: int
    limit: int
    offset: int


class ArchiveYear(BaseModel):
    year: int
    posts: list[PostSummary]
