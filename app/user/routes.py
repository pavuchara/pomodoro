from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Path,
    Depends,
)

from auth.dependencies import get_user_token_data
from user.exceptions import UserDoesNotExistException
from user.dependencies import get_user_service
from user.services import UserService
from user.schemas import (
    UserCreateScema,
    UserRetrieveSchema,
    UserUpdateSchema,
)


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=list[UserRetrieveSchema], status_code=status.HTTP_200_OK)
async def get_all_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_all_users()


@router.post("/", response_model=UserRetrieveSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateScema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(user_data)


@router.get("/me", response_model=UserRetrieveSchema, status_code=status.HTTP_200_OK)
async def get_current_user(
    current_user: Annotated[dict, Depends(get_user_token_data)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        return await user_service.get_user_by_id(current_user["id"])
    except UserDoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Авторизуйтесь",
        )


@router.get("/{user_id}", response_model=UserRetrieveSchema, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: Annotated[int, Path()],
    user_repository: Annotated[UserService, Depends(get_user_service)],
):
    if user := await user_repository.get_user_by_id(user_id):
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Пользователь не найден",
    )


@router.put("/{user_id}", response_model=UserRetrieveSchema, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: Annotated[int, Path()],
    user_data: UserUpdateSchema,
    user_repository: Annotated[UserService, Depends(get_user_service)],
):
    try:
        return await user_repository.update_user(user_id, user_data)
    except UserDoesNotExistException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
