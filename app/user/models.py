from sqlalchemy import (
    Integer,
    String,
    Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    validates,
    mapped_column,
)

from user.utils import (
    validate_user_email,
    validate_username,
)
from database.db import Base


class User(Base):
    __tablename__ = "users"
    # Fields:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(60))
    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(50), nullable=False)
    bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    # Relationships:
    # TODO realize

    @validates("email")
    def validate_email(self, _, value):
        return validate_user_email(value)

    @validates("username")
    def validate_username(self, _, value):
        return validate_username(value)
