from fastapi import APIRouter

from app.routers.health import router as health_router

__all__ = ["router"]

router = APIRouter(prefix="/api")

router.include_router(health_router)
