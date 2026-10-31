from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from mywebproject.api.serializers import to_post_detail, to_post_summary
from mywebproject.db import get_session
from mywebproject.models import Post, Tag
from mywebproject.schema.post import PostDetail, PostListResponse

router = APIRouter()


@router.get("", response_model=PostListResponse)
async def list_posts(
    session: Annotated[AsyncSession, Depends(get_session)],
    tag: str | None = None,
    q: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> PostListResponse:
    filters = []

    if tag:
        filters.append(Post.tags.any(Tag.name == tag))

    if q:
        keyword = q.strip()
        if keyword:
            pattern = f"%{keyword}%"
            filters.append(
                or_(Post.title.ilike(pattern), Post.summary.ilike(pattern))
            )

    total = await session.scalar(
        select(func.count(Post.id)).where(*filters)
    ) or 0

    statement = (
        select(Post)
        .where(*filters)
        .options(selectinload(Post.tags))
        .order_by(Post.published_on.desc(), Post.id.desc())
        .limit(limit)
        .offset(offset)
    )
    posts = (await session.scalars(statement)).all()

    return PostListResponse(
        items=[to_post_summary(post) for post in posts],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{slug}", response_model=PostDetail)
async def get_post(
    slug: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PostDetail:
    statement = (
        select(Post)
        .where(Post.slug == slug)
        .options(selectinload(Post.tags))
    )
    post = await session.scalar(statement)

    if post is None:
        raise HTTPException(status_code=404, detail="文章不存在")

    return to_post_detail(post)
