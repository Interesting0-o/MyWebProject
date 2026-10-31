import logging
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from mywebproject.models import Post, Tag
from mywebproject.seed_data import POSTS
from mywebproject.utils import estimate_reading_time

logger = logging.getLogger(__name__)


async def seed_posts(session: AsyncSession) -> int:
    post_count = await session.scalar(select(func.count(Post.id)))

    if post_count:
        logger.info("文章数据已存在，跳过示例数据写入（%s 篇）", post_count)
        return 0

    existing_tags = {
        tag.name: tag for tag in (await session.scalars(select(Tag))).all()
    }

    for item in POSTS:
        content = item["content"]
        post = Post(
            slug=item["slug"],
            title=item["title"],
            summary=item["summary"],
            content=content,
            reading_time=estimate_reading_time(content),
            published_on=date.fromisoformat(item["date"]),
        )

        for tag_name in item["tags"]:
            tag = existing_tags.get(tag_name)
            if tag is None:
                tag = Tag(name=tag_name)
                existing_tags[tag_name] = tag
            post.tags.append(tag)

        session.add(post)

    await session.commit()
    logger.info("已写入 %s 篇示例文章", len(POSTS))
    return len(POSTS)
