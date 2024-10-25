from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class CategoryCreateSchema(BaseModel):
    name: str = Field(max_length=255)


class CategoryRetrieveSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class TaskRetrieveSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    pomodoro_count: int
    category: CategoryRetrieveSchema


class TaskCreateSchema(BaseModel):
    name: str = Field(max_length=255)
    pomodoro_count: int = Field(ge=1, le=10)
    category_id: int = Field(ge=1)
