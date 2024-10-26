from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm

from auth.exceptions import AuthUserException
from auth.schemas import AccessTorenReponse
from auth.dependencies import get_auth_service
from auth.services import AuthServise


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", status_code=status.HTTP_200_OK, response_model=AccessTorenReponse)
async def get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthServise, Depends(get_auth_service)],
):
    try:
        user = await auth_service.authenticate_user(
            email=form_data.username,  # username -> email
            password=form_data.password,
        )
        access_token = await auth_service.create_access_token(user)
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    except AuthUserException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
