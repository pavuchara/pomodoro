from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from redis.asyncio import Redis

from database.db_depends import get_db_session
from database.cache_depends import get_cache_session
from tasks.services import TaskService
from tasks.repositories.db_query_repositories import (
    CategoryRepository,
    TaskRepository,
)
from tasks.repositories.cache_repositories import (
    TaskCacheRepository,
)


async def get_task_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> TaskRepository:
    return TaskRepository(db_session)


async def get_category_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> CategoryRepository:
    return CategoryRepository(db_session)


async def get_task_cache_repository(
    cache_session: Annotated[Redis, Depends(get_cache_session)]
) -> TaskCacheRepository:
    return TaskCacheRepository(cache_session)


async def get_tasks_servise(
    task_repository: Annotated[TaskRepository, Depends(get_task_repository)],
    cache_repository: Annotated[TaskCacheRepository, Depends(get_task_cache_repository)]
) -> TaskService:
    return TaskService(task_repository, cache_repository)
