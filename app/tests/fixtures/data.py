import pytest

from user.schemas import (
    UserCreateScema,
    UserUpdateSchema,
)


@pytest.fixture
async def correct_user_data_dict_create() -> dict:
    user_data = {
        "username": "correct_user",
        "email": "correct_user@gmail.com",
        "password": "some_password",
        "first_name": "Name",
        "last_name": "Lastname",
        "bio": "Some"
    }
    return user_data


@pytest.fixture
async def correct_user_data_schema_create(correct_user_data_dict_create) -> UserCreateScema:
    return UserCreateScema(**correct_user_data_dict_create)


@pytest.fixture
async def correct_user_data_dict_update() -> dict:
    user_data = {
        "username": "correct_user",
        "first_name": "Name",
        "last_name": "Lastname",
        "bio": "Some"
    }
    return user_data


@pytest.fixture
async def correct_user_data_schema_update(correct_user_data_dict_update) -> UserUpdateSchema:
    return UserUpdateSchema(**correct_user_data_dict_update)
