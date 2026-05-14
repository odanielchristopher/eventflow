from src.app import app
from src.core.config import get_settings


settings = get_settings()


def main() -> None:
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )


if __name__ == "__main__":
    main()
