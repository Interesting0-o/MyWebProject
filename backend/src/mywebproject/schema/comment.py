from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class CommentCreate(BaseModel):
    author_name: str = Field(min_length=2, max_length=40)
    content: str = Field(min_length=2, max_length=1000)

    @field_validator("author_name", "content")
    @classmethod
    def strip_and_validate(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("至少需要 2 个字符")
        return value


class CommentItem(BaseModel):
    id: int
    author_name: str
    content: str
    created_at: datetime
