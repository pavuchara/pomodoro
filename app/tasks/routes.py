from typing import Annotated

from fastapi import (
    APIRouter,
    status,
    Response,
    HTTPException,
    Depends,
    Path,
)
from sqlalchemy.exc import IntegrityError

from tasks.services import TaskService
from tasks.dependencies import (
    get_category_repository,
    get_tasks_servise,
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
):
    try:
        task = await task_service.create_task(task_data)
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
    task = await task_service.get_task(task_id)
    if task:
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Такого рецепта нет",
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: Annotated[int, Path()],
    task_service: Annotated[TaskService, Depends(get_tasks_servise)],
):
    await task_service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskRetrieveSchema)
async def update_task(
    task_id: Annotated[int, Path()],
    task_data: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_tasks_servise)],
):
    if task := await task_service.update_task(task_id, task_data):
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Такой задачи нет",
    )
