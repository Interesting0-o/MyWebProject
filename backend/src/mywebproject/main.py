from collections.abc import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mywebproject.api import api_router
from mywebproject.config import Settings, get_settings
from mywebproject.resource.path import ensure_runtime_dirs


async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    ensure_runtime_dirs()
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix="/api")

    @app.get("/", tags=["system"])
    def root() -> dict[str, str]:
        return {"message": "Backend is OK!"}

    return app


app = create_app()


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "mywebproject.main:app",
        host=settings.BACKEND_URL,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
    )
