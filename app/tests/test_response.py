import pytest

from fastapi import status

from httpx import AsyncClient

from user.schemas import UserCreateScema
from user.repositories import UserRepository

pytestmark = pytest.mark.asyncio


async def test_get_user_path(anonymous_client: AsyncClient):
    response = await anonymous_client.get("/user/")
    assert response.status_code == status.HTTP_200_OK


async def test_post_user_path(
    anonymous_client: AsyncClient,
    user_repository: UserRepository,
    correct_user_data_schema_create: UserCreateScema,
):
    response = await anonymous_client.post(
        "/user/",
        data=correct_user_data_schema_create.model_dump_json()
    )
    assert response.status_code == status.HTTP_201_CREATED
    users = await user_repository.get_all_users()
    assert len(users) == 1
