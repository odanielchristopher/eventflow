from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.staticfiles import StaticFiles
from scalar_fastapi import get_scalar_api_reference

from src.core.config import get_settings
from src.routes import document_router
from src.routes import event_router
from src.routes import hash_router
from src.routes import subscription_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger("uvicorn.error")
    settings.resolved_upload_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Documentacao disponivel em http://localhost:3000/docs")
    logger.info("Banco ativo configurado para %s", "SQLite" if settings.is_sqlite else "PostgreSQL")
    yield


def create_app() -> FastAPI:
    settings.resolved_upload_dir.mkdir(parents=True, exist_ok=True)
    app = FastAPI(
        title="EventFlow API",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    app.include_router(document_router)
    app.include_router(event_router)
    app.include_router(hash_router)
    app.include_router(subscription_router)
    app.mount("/uploads", StaticFiles(directory=settings.resolved_upload_dir), name="uploads")
    add_pagination(app)

    @app.get("/")
    def root() -> dict[str, str]:
        return {"message": "EventFlow API is running"}
    
    @app.get("/docs", include_in_schema=False)
    async def scalar():
        return get_scalar_api_reference(
            openapi_url=app.openapi_url,
            title="EventFlow API"
        )

    return app


app = create_app()
