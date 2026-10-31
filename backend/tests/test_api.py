import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from mywebproject.api import api_router
from mywebproject.db import get_session
from mywebproject.models import Base
from mywebproject.seed import seed_posts
from mywebproject.utils import estimate_reading_time


@asynccontextmanager
async def create_test_client() -> AsyncIterator[AsyncClient]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        await seed_posts(session)

    app = FastAPI()
    app.include_router(api_router, prefix="/api")

    async def override_get_session() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    await engine.dispose()


def test_health() -> None:
    async def scenario() -> None:
        async with create_test_client() as client:
            response = await client.get("/api/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    asyncio.run(scenario())


def test_list_posts() -> None:
    async def scenario() -> None:
        async with create_test_client() as client:
            response = await client.get("/api/posts")

        assert response.status_code == 200
        payload = response.json()
        assert payload["total"] == 6
        assert payload["limit"] == 20
        assert payload["offset"] == 0
        assert len(payload["items"]) == 6
        assert payload["items"][0]["slug"] == "vue-3-composition-refactor"
        assert payload["items"][0]["date"] == "2026-10-24"
        assert payload["items"][0]["tags"] == ["Vue", "前端"]
        assert all(item["reading_time"] >= 1 for item in payload["items"])

    asyncio.run(scenario())


def test_filter_and_pagination() -> None:
    async def scenario() -> None:
        async with create_test_client() as client:
            by_tag = await client.get("/api/posts", params={"tag": "Vue"})
            by_keyword = await client.get("/api/posts", params={"q": "FastAPI"})
            paged = await client.get("/api/posts", params={"limit": 2, "offset": 4})

        assert by_tag.status_code == 200
        assert by_tag.json()["total"] == 1
        assert by_tag.json()["items"][0]["slug"] == "vue-3-composition-refactor"

        assert by_keyword.status_code == 200
        assert by_keyword.json()["total"] == 2

        assert paged.status_code == 200
        assert paged.json()["total"] == 6
        assert len(paged.json()["items"]) == 2

    asyncio.run(scenario())


def test_post_detail_and_not_found() -> None:
    async def scenario() -> None:
        async with create_test_client() as client:
            detail = await client.get("/api/posts/vue-3-composition-refactor")
            missing = await client.get("/api/posts/not-found")

        assert detail.status_code == 200
        payload = detail.json()
        assert payload["title"] == "用 Vue 3 组合式 API 重构一个旧页面"
        assert payload["content"][0]["type"] == "paragraph"
        assert len(payload["content"]) == 16

        assert missing.status_code == 404
        assert missing.json() == {"detail": "文章不存在"}

    asyncio.run(scenario())


def test_tags_and_archive() -> None:
    async def scenario() -> None:
        async with create_test_client() as client:
            tags = await client.get("/api/tags")
            archive = await client.get("/api/archive")

        assert tags.status_code == 200
        tag_counts = {tag["name"]: tag["count"] for tag in tags.json()}
        assert len(tag_counts) == 12
        assert tag_counts["Vue"] == 1

        assert archive.status_code == 200
        archive_payload = archive.json()
        assert [group["year"] for group in archive_payload] == [2026, 2025]
        assert sum(len(group["posts"]) for group in archive_payload) == 6

    asyncio.run(scenario())


def test_comments() -> None:
    async def scenario() -> None:
        async with create_test_client() as client:
            slug = "/api/posts/vue-3-composition-refactor/comments"
            empty = await client.get(slug)
            created = await client.post(
                slug,
                json={"author_name": "  读者  ", "content": "  很有帮助，感谢分享。  "},
            )
            listed = await client.get(slug)
            missing = await client.get("/api/posts/not-found/comments")
            invalid = await client.post(
                slug,
                json={"author_name": "a", "content": "x"},
            )

        assert empty.status_code == 200
        assert empty.json() == []

        assert created.status_code == 201
        payload = created.json()
        assert payload["author_name"] == "读者"
        assert payload["content"] == "很有帮助，感谢分享。"
        assert payload["created_at"]

        assert listed.status_code == 200
        assert [item["id"] for item in listed.json()] == [payload["id"]]

        assert missing.status_code == 404
        assert invalid.status_code == 422

    asyncio.run(scenario())


def test_seed_is_idempotent() -> None:
    async def scenario() -> None:
        engine = create_async_engine(
            "sqlite+aiosqlite://",
            poolclass=StaticPool,
        )

        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        session_factory = async_sessionmaker(engine, expire_on_commit=False)

        async with session_factory() as session:
            assert await seed_posts(session) == 6
            assert await seed_posts(session) == 0

        await engine.dispose()

    asyncio.run(scenario())


def test_estimate_reading_time() -> None:
    assert estimate_reading_time([{"type": "paragraph", "text": "很短的一段话。"}]) == 1
    assert estimate_reading_time([{"type": "paragraph", "text": "中" * 600}]) == 2
