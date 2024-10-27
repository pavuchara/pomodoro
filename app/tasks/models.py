from sqlalchemy import (
    Integer,
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    validates,
    relationship,
    mapped_column,
)

from database.db import Base
from tasks.exceptions import TaskValidationException


class Task(Base):
    __tablename__ = "tasks"
    # Fields:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    pomodoro_count: Mapped[int] = mapped_column(Integer)
    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        index=True,
    )
    # Relationships:
    author = relationship(
        "User",
        back_populates="tasks",
        passive_deletes=True,
        lazy="joined",
    )
    category = relationship(
        "Category",
        back_populates="tasks",
        passive_deletes=True,
        lazy="joined",
    )

    @validates("pomodoro_count")
    def validate_pomodoro_count(self, _, value):
        if not 1 <= value <= 10:
            raise TaskValidationException("Значение должно быть от 1 до 10")
        return value


class Category(Base):
    __tablename__ = "categories"
    # Fields:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    # Relationships:
    tasks = relationship(
        "Task",
        back_populates="category",
        cascade="all, delete-orphan",
    )
