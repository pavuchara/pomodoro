from typing import AsyncGenerator

import redis.asyncio as redis

from settings import (
    REDIS_HOST,
    REDIS_PORT,
)


async def get_cache_session() -> AsyncGenerator[redis.Redis, None]:
    cache_session = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        yield cache_session
    finally:
        await cache_session.aclose()
