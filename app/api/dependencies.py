from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository.content import ContentRepository
from app.db.repository.device import DeviceRepository
from app.db.repository.protection_system import ProtectionSystemRepository
from app.db.session import DatabaseSessionManager


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_manager = DatabaseSessionManager()
    try:
        async with session_manager.get_async_session() as session:
            yield session
    finally:
        await session_manager.close()


def get_protection_system_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> ProtectionSystemRepository:
    return ProtectionSystemRepository(db_session=db_session)


def get_content_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> ContentRepository:
    return ContentRepository(db_session=db_session)


def get_device_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> DeviceRepository:
    return DeviceRepository(db_session=db_session)
