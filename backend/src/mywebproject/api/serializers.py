from mywebproject.models import Post
from mywebproject.schema.post import PostDetail, PostSummary


def to_post_summary(post: Post) -> PostSummary:
    return PostSummary(
        slug=post.slug,
        title=post.title,
        summary=post.summary,
        date=post.published_on,
        tags=[tag.name for tag in post.tags],
        reading_time=post.reading_time,
    )


def to_post_detail(post: Post) -> PostDetail:
    return PostDetail(
        **to_post_summary(post).model_dump(),
        content=post.content,
    )
