import pytest
from fastapi import APIRouter, FastAPI
from starlette.testclient import TestClient

from app.api.routers import router as api_router
from app.db.session import DatabaseSessionManager
from app.main import app as api_app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def app() -> FastAPI:
    return api_app


@pytest.fixture
def router() -> APIRouter:
    return api_router


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
async def db_session():
    from app.db.models.base import BaseModel

    session_manager = DatabaseSessionManager()

    async with session_manager.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    try:
        async with session_manager.get_async_session() as session:
            yield session
    finally:
        async with session_manager.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
        await session_manager.close()
