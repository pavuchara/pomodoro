from fastapi import APIRouter


router = APIRouter(prefix="/ping", tags=["ping"])


# TODO realize
@router.get("/app")
async def ping_app():
    return {"message": "OK"}


# TODO realize
@router.get("/db")
async def ping_db():
    return {"message": "OK"}


# TODO realize
@router.get("/cache")
async def ping_cache():
    return {"message": "OK"}
