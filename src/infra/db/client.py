from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.infra.db.session import engine, session_factory


class DatabaseClient:
    def __init__(
        self,
        engine: AsyncEngine,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self.engine = engine
        self.session_factory = session_factory

    def session(self) -> async_sessionmaker[AsyncSession]:
        return self.session_factory


db_client = DatabaseClient(engine=engine, session_factory=session_factory)
