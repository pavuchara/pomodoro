from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import get_object_or_404
from tasks.models import (
    Category,
    Task,
)
from tasks.schemas import (
    TaskCreateSchema,
    CategoryCreateSchema,
)


class TaskRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all_tasks(self) -> Sequence[Task]:
        query = select(Task)
        all_tasks = await self.db.scalars(query)
        return all_tasks.all()

    async def get_task_by_id(self, task_id: int) -> Task | None:
        query = (
            select(Task)
            .where(Task.id == task_id)
        )
        task = await self.db.scalar(query)
        return task

    async def create_task(self, task_data: TaskCreateSchema, user_id: int) -> Task:
        category = await get_object_or_404(self.db, Category, Category.id == task_data.category_id)
        task = Task(
            name=task_data.name,
            pomodoro_count=task_data.pomodoro_count,
            category_id=category.id,
            author_id=user_id,
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()

    async def update_task(self, task: Task, task_data: TaskCreateSchema) -> Task:
        category = await get_object_or_404(self.db, Category, Category.id == task_data.category_id)
        task.name = task_data.name
        task.pomodoro_count = task_data.pomodoro_count
        task.category_id = category.id
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task


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
