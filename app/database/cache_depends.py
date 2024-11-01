from typing import AsyncGenerator

from redis.asyncio import Redis

from settings import (
    REDIS_HOST,
    REDIS_PORT,
)


async def get_cache_session() -> AsyncGenerator[Redis, None]:
    cache_session = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        yield cache_session
    finally:
        await cache_session.aclose()
