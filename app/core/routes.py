from fastapi import APIRouter


router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/app")
async def ping_app():
    return {"message": "OK"}


@router.get("/db")
async def ping_db():
    return {"message": "OK"}
