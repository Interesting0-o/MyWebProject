from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from mywebproject.db import get_session
from mywebproject.models import Tag, post_tags
from mywebproject.schema.tag import TagRead

router = APIRouter()


@router.get("", response_model=list[TagRead])
async def list_tags(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[TagRead]:
    count = func.count(post_tags.c.post_id)
    statement = (
        select(Tag.name, count.label("post_count"))
        .join(post_tags, Tag.id == post_tags.c.tag_id)
        .group_by(Tag.id, Tag.name)
        .order_by(count.desc(), Tag.name)
    )
    rows = (await session.execute(statement)).all()

    return [TagRead(name=name, count=post_count) for name, post_count in rows]
