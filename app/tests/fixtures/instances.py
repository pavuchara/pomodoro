import pytest

from user.services import UserService


@pytest.fixture
async def correct_user_data(user_service: UserService, correct_user_data):
    user = await user_service.create_user(correct_user_data)
    return user
