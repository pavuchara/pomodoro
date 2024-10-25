from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import get_object_or_404
from tasks.models import (
    Category,
    Task,
)
from tasks.schemas import (
    TaskCreateSchema,
    TaskRetrieveSchema,
    CategoryCreateSchema,
)


class TaskRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all_tasks(self) -> Sequence[Task]:
        query = (
            select(Task)
            .options(
                joinedload(Task.category)
            )
        )
        all_tasks = await self.db.scalars(query)
        return all_tasks.all()

    async def get_task_by_id(self, task_id: int) -> Task | None:
        query = (
            select(Task)
            .where(Task.id == task_id)
            .options(
                joinedload(Task.category)
            )
        )
        task = await self.db.scalar(query)
        return task

    async def create_task(self, task_data: TaskCreateSchema) -> Task:
        category = await get_object_or_404(self.db, Category, Category.id == task_data.category_id)
        task = Task(
            name=task_data.name,
            pomodoro_count=task_data.pomodoro_count,
            category_id=category.id,
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: int) -> None:
        task = get_object_or_404(self.db, Task, Task.id == task_id)
        if task:
            await self.db.delete(task)
            await self.db.commit()

    async def update_task(self, task_id: int, task_data: TaskCreateSchema) -> Task | None:
        task = await self.get_task_by_id(task_id)
        category = await get_object_or_404(self.db, Category, Category.id == task_data.category_id)
        if not task:
            return None
        task.name = task_data.name
        task.pomodoro_count = task_data.pomodoro_count
        task.category_id = category.id
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def to_schema(
        self,
        joinloaded_objects: Sequence[Task] | Task,
        many: bool = False,
    ):
        if many:
            return [
                TaskRetrieveSchema.model_validate(task)
                for task in joinloaded_objects  # type:ignore
            ]
        return TaskRetrieveSchema.model_validate(joinloaded_objects)


class CategoryRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all_categories(self) -> Sequence[Category]:
        query = select(Category)
        categories = await self.db.scalars(query)
        return categories.all()

    async def get_category_by_id(self, category_id: int) -> Category | None:
        query = select(Category).where(Category.id == category_id)
        category = await self.db.scalar(query)
        return category

    async def create_category(self, category_data: CategoryCreateSchema) -> Category:
        category = Category(
            name=category_data.name,
        )
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category
