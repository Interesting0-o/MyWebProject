from fastapi import APIRouter

from mywebproject.api import archive, posts, tags
from mywebproject.schema.health import HealthResponse

api_router = APIRouter()

api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(archive.router, tags=["archive"])


@api_router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok")
