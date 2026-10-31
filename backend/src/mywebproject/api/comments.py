from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mywebproject.api.serializers import to_comment
from mywebproject.db import get_session
from mywebproject.models import Comment, Post
from mywebproject.schema.comment import CommentCreate, CommentItem

router = APIRouter()


async def get_post_or_404(slug: str, session: AsyncSession) -> Post:
    post = await session.scalar(select(Post).where(Post.slug == slug))
    if post is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    return post


@router.get("/{slug}/comments", response_model=list[CommentItem])
async def list_comments(
    slug: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[CommentItem]:
    post = await get_post_or_404(slug, session)
    statement = (
        select(Comment)
        .where(
            Comment.post_id == post.id,
            Comment.is_approved.is_(True),
        )
        .order_by(Comment.created_at.asc(), Comment.id.asc())
    )
    comments = (await session.scalars(statement)).all()

    return [to_comment(comment) for comment in comments]


@router.post(
    "/{slug}/comments",
    response_model=CommentItem,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    slug: str,
    payload: CommentCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CommentItem:
    post = await get_post_or_404(slug, session)
    comment = Comment(
        post_id=post.id,
        author_name=payload.author_name,
        content=payload.content,
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return to_comment(comment)
