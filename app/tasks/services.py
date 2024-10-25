from tasks.schemas import TaskCreateSchema, TaskRetrieveSchema

from tasks.repositories.db_query_repositories import (
    TaskRepository,
)
from tasks.repositories.cache_repositories import (
    TaskCacheRepository,
)


class TaskService:

    def __init__(
        self,
        task_repository: TaskRepository,
        task_cache_repository: TaskCacheRepository,
    ) -> None:
        self.task_repository = task_repository
        self.task_cache_repository = task_cache_repository

    async def get_all_tasks(self) -> list[TaskRetrieveSchema]:
        if cached_tasks := await self.task_cache_repository.get_all_tasks("all_tasks"):
            return cached_tasks
        all_tasks = await self.task_repository.get_all_tasks()
        tasks_to_schema = await self.task_repository.to_schema(all_tasks, many=True)
        await self.task_cache_repository.set_all_tasks(tasks_to_schema)
        return tasks_to_schema

    async def get_task(self, task_id: int) -> TaskRetrieveSchema | None:
        task = await self.task_repository.get_task_by_id(task_id)
        if not task:
            return None
        return await self.task_repository.to_schema(task)

    async def create_task(self, task_data: TaskCreateSchema) -> TaskRetrieveSchema:
        task = await self.task_repository.create_task(task_data)
        await self.task_cache_repository.invalidate_all_tasks()
        return await self.task_repository.to_schema(task)

    async def delete_task(self, task_id: int) -> None:
        await self.task_repository.delete_task(task_id)
        await self.task_cache_repository.invalidate_all_tasks()

    async def update_task(
        self,
        task_id: int,
        task_data: TaskCreateSchema
    ) -> TaskRetrieveSchema | None:
        if task := await self.task_repository.update_task(task_id, task_data):
            await self.task_cache_repository.invalidate_all_tasks()
            return await self.task_repository.to_schema(task)
        return None
