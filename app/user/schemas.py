from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationInfo,
    Field,
    field_validator,
)

from user.exceptions import UserValidationException
from user.utils import validate_user_email, validate_username


class UserAuthSchema(BaseModel):
    email: str = Field(max_length=256)
    password: str = Field(max_length=50)

    @field_validator("email")
    @classmethod
    def validate_email_field(cls, value: str, info: ValidationInfo):
        try:
            return validate_user_email(value)
        except UserValidationException as e:
            raise ValueError(str(e))


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(max_length=50)
    first_name: str | None = Field(max_length=50)
    last_name: str | None = Field(max_length=50)
    bio: str | None = Field(max_length=1000)

    @field_validator("username")
    @classmethod
    def validate_username_field(cls, value: str, info: ValidationInfo):
        try:
            return validate_username(value)
        except UserValidationException as e:
            raise ValueError(str(e))


class UserCreateScema(UserUpdateSchema, UserAuthSchema):
    pass


class UserRetrieveSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    bio: str
