from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from auth.services import AuthServise
from user.dependencies import get_user_repository
from user.repositories import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> AuthServise:
    return AuthServise(user_repository)


async def get_user_token_data(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthServise, Depends(get_auth_service)],
):
    return await auth_service.decode_token(token)
