import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import config
from app.api.routers import router
from app.db.session import DatabaseSessionManager


@asynccontextmanager
async def _app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # TODO: Delete once real DB and migrations are implemented

    from app.db.models.base import BaseModel

    session_manager = DatabaseSessionManager()

    async with session_manager.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield
    await session_manager.close()


app = FastAPI(
    title="Demo App Api",
    version="0.1.0",
    debug=config.DEBUG,
    docs_url="/docs" if config.DEBUG else None,
    redoc_url=None,
    lifespan=_app_lifespan,
)

app.include_router(router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
