import pytest

from user.repositories import UserRepository
from user.services import UserService
from tasks.repositories.db_query_repositories import (
    CategoryRepository,
    TaskRepository,
)
from tasks.services import TaskService


@pytest.fixture
async def user_repository(db_session) -> UserRepository:
    return UserRepository(db_session)


@pytest.fixture
async def task_repository(db_session) -> TaskRepository:
    return TaskRepository(db_session)


@pytest.fixture
async def category_repository(db_session) -> CategoryRepository:
    return CategoryRepository(db_session)


@pytest.fixture
async def user_service(user_repository) -> UserService:
    return UserService(user_repository)


@pytest.fixture
async def task_service(task_repository) -> TaskService:
    return TaskService(task_repository)
