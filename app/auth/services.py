from datetime import datetime, timezone
from typing import Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from auth.exceptions import AuthUserException
from user.models import User
from user.repositories import UserRepository
from settings import (
    ACCESS_TOKEN_LIFETIME,
    ALGORITHM,
    SECRET_KEY,
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthServise:

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.user_repository.get_user_by_email(email)
        if not user or (user and not bcrypt_context.verify(password, user.password)):
            raise AuthUserException(
                "Введенные креды невалидны или такого пользователя не существует"
            )
        return user

    @staticmethod
    async def create_access_token(user: User) -> str:
        encode = {
            "id": user.id,
            "email": user.email,
            "is_admin": user.is_admin,
        }
        expires = datetime.now(timezone.utc) + ACCESS_TOKEN_LIFETIME
        encode.update({"exp": expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    async def decode_token(token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        except JWTError:
            raise AuthUserException("Не получилось валидировать креды или токен истек")
