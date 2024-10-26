from user.exceptions import UserDoesNotExistException
from user.repositories import UserRepository
from user.schemas import UserCreateScema, UserUpdateSchema


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_all_users(self):
        return await self.user_repository.get_all_users()

    async def get_user_by_id(self, user_id: int):
        if user := await self.user_repository.get_user_by_id(user_id):
            return user
        raise UserDoesNotExistException()

    async def create_user(self, user_data: UserCreateScema):
        return await self.user_repository.create_user(user_data)

    async def update_user(self, user_id: int, user_data: UserUpdateSchema):
        return await self.user_repository.update_user(user_id, user_data)
