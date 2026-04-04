from __future__ import annotations

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from src.routes import event_router
from src.routes import hash_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="EventFlow API",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )
    app.include_router(event_router)
    app.include_router(hash_router)

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
