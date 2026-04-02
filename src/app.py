from __future__ import annotations

from fastapi import FastAPI

from src.routes import event_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="EventFlow API",
        version="0.1.0",
    )
    app.include_router(event_router)

    @app.get("/")
    def root() -> dict[str, str]:
        return {"message": "EventFlow API is running"}

    return app


app = create_app()
