from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_depends import get_db_session
from user.services import UserService
from user.repositories import UserRepository


async def get_user_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserRepository:
    return UserRepository(db_session)


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(user_repository)
