import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, Response
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", name="health", description="Health check")
async def health(db_session: AsyncSession = Depends(get_db_session)) -> Response:
    try:
        await db_session.execute(text("SELECT 1"))
    except Exception:
        logger.exception("Database health check failed")
        return Response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content="Database health check failed")

    return Response(status_code=HTTPStatus.OK, content="OK")
