from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_depends import get_db_session
from user.services import UserService
from user.repositories import UserRepository

from services.dependencies import get_mail_client_service
from services.email_service.mailing import MailService


async def get_user_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserRepository:
    return UserRepository(db_session)


async def get_mail_service(
    mail_service: Annotated[MailService, Depends(get_mail_client_service)],
) -> MailService:
    return mail_service


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    mail_service: Annotated[MailService, Depends(get_mail_service)],
) -> UserService:
    return UserService(user_repository=user_repository, mail_service=mail_service)
