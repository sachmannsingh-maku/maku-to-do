from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_db
from .service import SystemService

router = APIRouter(tags=["System"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def check_db_health(db: AsyncSession = Depends(get_db)):
    db_ok = await SystemService.check_database(db)
    if not db_ok:
        return {
            "status": "unhealthy",
            "database": "down"
        }

    return {
        "status": "healthy",
        "database": "up"
    }