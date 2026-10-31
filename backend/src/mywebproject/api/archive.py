from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from mywebproject.api.serializers import to_post_summary
from mywebproject.db import get_session
from mywebproject.models import Post
from mywebproject.schema.post import ArchiveYear, PostSummary

router = APIRouter()


@router.get("/archive", response_model=list[ArchiveYear])
async def list_archive(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[ArchiveYear]:
    statement = (
        select(Post)
        .options(selectinload(Post.tags))
        .order_by(Post.published_on.desc(), Post.id.desc())
    )
    posts = (await session.scalars(statement)).all()

    grouped: dict[int, list[PostSummary]] = {}
    for post in posts:
        grouped.setdefault(post.published_on.year, []).append(
            to_post_summary(post)
        )

    return [
        ArchiveYear(year=year, posts=items) for year, items in grouped.items()
    ]
