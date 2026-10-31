from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from mywebproject.config import get_settings
from mywebproject.models import Base
from mywebproject.seed import seed_posts

engine: AsyncEngine = create_async_engine(
    get_settings().DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"charset": "utf8mb4"},
)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def check_database_connection() -> None:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


async def initialize_database(*, seed: bool = True) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    if seed:
        async with async_session_factory() as session:
            await seed_posts(session)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session


async def close_database_connection() -> None:
    await engine.dispose()
