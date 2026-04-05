from src.app import app


def main() -> None:
    import uvicorn

    uvicorn.run("main:app", port=3000, reload=True)


if __name__ == "__main__":
    main()
