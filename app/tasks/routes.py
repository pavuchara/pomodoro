from typing import Annotated, Any

from fastapi import (
    APIRouter,
    status,
    Response,
    HTTPException,
    Depends,
    Path,
)
from sqlalchemy.exc import IntegrityError

from auth.dependencies import get_user_token_data
from tasks.services import TaskService
from tasks.dependencies import (
    get_category_repository,
    get_tasks_servise,
)
from tasks.exceptions import (
    TaskDoesnotExistsException,
    TaskOnlyAuthorException,
)
from tasks.repositories.db_query_repositories import (
    CategoryRepository,
)
from tasks.schemas import (
    CategoryCreateSchema,
    CategoryRetrieveSchema,
    TaskCreateSchema,
    TaskRetrieveSchema,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
    "/",
    response_model=list[TaskRetrieveSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_tasks(
    task_service: Annotated[TaskService, Depends(get_tasks_servise)],
):
    return await task_service.get_all_tasks()


@router.post("/", response_model=TaskRetrieveSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_tasks_servise)],
    current_user_data: Annotated[dict, Depends(get_user_token_data)]
):
    try:
        user_id: int = current_user_data["id"]
        task = await task_service.create_task(task_data, user_id)
        return task
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проверьте данные, что-то пошло не так.",
        )


@router.get(
    "/categories",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryRetrieveSchema],
)
async def get_all_categories(
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)],
):
    return await category_repository.get_all_categories()


@router.post(
    "/categories",
    response_model=CategoryRetrieveSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_data: CategoryCreateSchema,
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)],
):
    try:
        return await category_repository.create_category(category_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проверьте данные, что-то пошло не так.",
        )


@router.get(
    "/categories/{category_id}",
    response_model=CategoryRetrieveSchema,
    status_code=status.HTTP_200_OK,
)
async def get_category(
    category_id: int,
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)],
):
    category = await category_repository.get_category_by_id(category_id)
    if category:
        return category
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Такой категории нет",
    )


@router.get(
    "/{task_id}",
    response_model=TaskRetrieveSchema,
    status_code=status.HTTP_200_OK,
)
async def get_task(
    task_id: Annotated[int, Path()],
    task_service: Annotated[TaskService, Depends(get_tasks_servise)],
):
    try:
        return await task_service.get_task(task_id)
    except TaskDoesnotExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: Annotated[int, Path()],
    task_service: Annotated[TaskService, Depends(get_tasks_servise)],
    current_user_data: Annotated[dict[str, Any], Depends(get_user_token_data)],
):
    try:
        user_id: int = current_user_data["id"]
        await task_service.delete_task(task_id, user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except TaskOnlyAuthorException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except TaskDoesnotExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskRetrieveSchema)
async def update_task(
    task_id: Annotated[int, Path()],
    task_data: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_tasks_servise)],
    current_user_data: Annotated[dict[str, Any], Depends(get_user_token_data)],
):
    try:
        user_id: int = current_user_data["id"]
        task = await task_service.update_task(task_id, task_data, user_id)
        return task
    except TaskOnlyAuthorException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except TaskDoesnotExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
