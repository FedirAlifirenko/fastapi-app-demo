from fastapi import APIRouter

from app.api.routers.content import router as content_router
from app.api.routers.health import router as health_router
from app.api.routers.protection_system import router as protection_system_router

__all__ = ["router"]

router = APIRouter(prefix="/api")

router.include_router(health_router)
router.include_router(content_router)
router.include_router(protection_system_router)
