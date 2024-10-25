import json

from redis.asyncio import Redis

from tasks.schemas import TaskRetrieveSchema


class TaskCacheRepository:

    def __init__(self, cache_session: Redis) -> None:
        self.cache_session = cache_session

    async def get_all_tasks(self, key: str = "all_tasks") -> list[TaskRetrieveSchema] | None:
        tasks_json = await self.cache_session.get(key)
        if tasks_json is None:
            return None
        return [TaskRetrieveSchema.model_validate(task) for task in json.loads(tasks_json)]

    async def set_all_tasks(
        self,
        tasks: list[TaskRetrieveSchema],
        key: str = "all_tasks"
    ) -> None:
        tasks_json = json.dumps([task.model_dump() for task in tasks], ensure_ascii=False)
        await self.cache_session.set(key, tasks_json, ex=60)

    async def invalidate_all_tasks(self, key: str = "all_tasks") -> None:
        await self.cache_session.delete(key)
