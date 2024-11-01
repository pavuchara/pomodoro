import pytest

from auth.services import bcrypt_context
from user.repositories import UserRepository
from user.schemas import (
    UserCreateScema,
    UserUpdateSchema,
)
from tasks.repositories.db_query_repositories import (
    CategoryRepository,
    TaskRepository,
)


pytestmark = pytest.mark.asyncio


async def test_empty_base(
    user_repository: UserRepository,
    task_repository: TaskRepository,
    category_repository: CategoryRepository,
):
    users = await user_repository.get_all_users()
    tasks = await task_repository.get_all_tasks()
    categories = await category_repository.get_all_categories()
    assert users == []
    assert tasks == []
    assert categories == []


async def test_correct_user_creation(
    correct_user_data_schema_create: UserCreateScema,
    user_repository: UserRepository,
):
    user_data = correct_user_data_schema_create

    user = await user_repository.create_user(user_data)
    new_user = await user_repository.get_user_by_id(user.id)
    assert new_user is not None
    assert new_user.email == user_data.email
    assert new_user.username == user_data.username
    assert new_user.first_name == user_data.first_name
    assert new_user.last_name == user_data.last_name
    assert bcrypt_context.verify(user_data.password, new_user.password) is True


async def test_correct_user_update(
    correct_user_data_schema_create: UserCreateScema,
    correct_user_data_schema_update: UserUpdateSchema,
    user_repository: UserRepository,
):
    new_user_data = correct_user_data_schema_update

    old_user = await user_repository.create_user(correct_user_data_schema_create)
    new_user = await user_repository.update_user(old_user.id, new_user_data)
    assert new_user is not None
    assert new_user.username == new_user_data.username
    assert new_user.first_name == new_user_data.first_name
    assert new_user.last_name == new_user_data.last_name
    assert old_user.email == new_user.email
    assert old_user.password == new_user.password
