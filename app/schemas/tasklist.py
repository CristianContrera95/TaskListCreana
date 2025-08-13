from pydantic import BaseModel

from app.models.tasklist import TaskPriority, TaskStatus


class TaskListCreateBody(BaseModel):
    """
    Basic schema to create a new user
    """

    title: str | None = None
    description: str


class TaskListUpdateBody(BaseModel):
    """
    Basic schema to update a new user
    """

    title: str | None = None
    description: str | None = None


class TaskCreateBody(BaseModel):
    """
    Basic schema to create a new user
    """

    title: str
    description: str | None = None
    status: TaskStatus | None = TaskStatus.pending
    priority: TaskPriority | None = TaskPriority.medium


class TaskUpdateBody(BaseModel):
    """
    Basic schema to update a new user
    """

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
