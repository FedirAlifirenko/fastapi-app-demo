import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app import config

logger = logging.getLogger(__name__)

__all__ = [
    "DatabaseSessionManager",
]


class DatabaseSessionManager:
    def __init__(
        self,
        *,
        engine: AsyncEngine | None = None,
        session_maker: async_sessionmaker[AsyncSession] | None = None,
    ):
        self._engine: AsyncEngine = engine or create_async_engine(
            config.DATABASE_URL,
            pool_pre_ping=True,
            echo=config.SQLALCHEMY_ECHO,
        )
        self._session_maker = session_maker or async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @asynccontextmanager
    async def get_async_session(self) -> AsyncIterator[AsyncSession]:
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            logger.error(f"Rollback due to error: {err}")
            await session.rollback()
            raise err
        finally:
            # copied from session.__aexit__() method
            task = asyncio.create_task(session.close())
            await asyncio.shield(task)

    async def close(self) -> None:
        task = asyncio.create_task(self._engine.dispose())
        await asyncio.shield(task)
