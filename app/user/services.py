from user.exceptions import UserDoesNotExistException
from user.repositories import UserRepository
from user.schemas import UserCreateScema, UserUpdateSchema

from services.email_service.mailing import MailService


class UserService:

    def __init__(
        self,
        user_repository: UserRepository,
        mail_service: MailService,
    ) -> None:
        self.user_repository = user_repository
        self.mail_service = mail_service

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

    async def send_email(self, to: str, email_text: str, subject: str) -> None:
        await self.mail_service.send_email(to, email_text, subject)
