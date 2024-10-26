from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from user.exceptions import UserDoesNotExistException
from user.models import User
from user.schemas import (
    UserCreateScema,
    UserUpdateSchema,
)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all_users(self) -> Sequence[User]:
        query = select(User)
        users = await self.db.scalars(query)
        return users.all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        user = await self.db.scalar(query)
        return user

    async def create_user(self, user_data: UserCreateScema) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            password=bcrypt_context.hash(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            bio=user_data.bio,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user_id: int, user_data: UserUpdateSchema) -> User | None:
        user = await self.get_user_by_id(user_id)
        if user:
            user.username = user_data.username
            user.first_name = user_data.first_name
            user.last_name = user_data.last_name
            user.bio = user_data.bio
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        raise UserDoesNotExistException()
