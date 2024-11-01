from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
)
from redis.asyncio import Redis
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_depends import get_db_session
from database.cache_depends import get_cache_session

router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/app")
async def ping_app():
    return {"message": "OK"}


@router.get("/db")
async def ping_db(db: Annotated[AsyncSession, Depends(get_db_session)]):
    try:
        await db.execute(text("SELECT 1"))
        return {"message": "OK"}
    except Exception:
        raise HTTPException(status_code=500, detail="DB connection failed")


@router.get("/cache")
async def ping_cache(cache_session: Annotated[Redis, Depends(get_cache_session)]):
    try:
        await cache_session.ping()
        return {"message": "OK"}
    except Exception:
        raise HTTPException(status_code=500, detail="Cache connection failed")
