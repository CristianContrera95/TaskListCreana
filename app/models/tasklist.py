import uuid
from enum import Enum

from pydantic import ConfigDict
from sqlmodel import Field, Relationship

from app.models import BaseSQLModel
from app.models.user import User


class TaskStatus(str, Enum):
    pending = "pending"
    done = "done"
    deprecated = "deprecated"


class TaskPriority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class TaskList(BaseSQLModel, table=True):
    __tablename__ = "task_lists"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    title: str = Field(default="TaskList", max_length=255)
    description: str | None = Field(default=None)

    tasks: list["Task"] | None = Relationship(
        back_populates="tasklist", cascade_delete=True
    )


class Task(BaseSQLModel, table=True):
    __tablename__ = "tasks"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)

    title: str = Field(description="Task title", max_length=255)
    description: str | None = Field(
        description="Task description details", default=None
    )
    status: TaskStatus = Field(
        description="Task completion status. Can be pending, done, deprecated",
        default=TaskStatus.pending,
    )
    priority: TaskPriority = Field(
        description="priority status. Can be high, medium or low (default: medium)",
        default=TaskPriority.medium,
    )

    tasklist_id: uuid.UUID = Field(
        description="TaskList father", foreign_key="task_lists.id"
    )
    assignee_id: uuid.UUID | None = Field(default=None, foreign_key="users.id")

    tasklist: TaskList | None = Relationship(back_populates="tasks")
    assignee: User | None = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={"foreign_keys": "[Task.assignee_id]"},
    )
