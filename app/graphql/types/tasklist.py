import uuid
from datetime import datetime

import strawberry as sb

from app.graphql.types.user import UserType
from app.models.tasklist import TaskPriority, TaskStatus


@sb.type
class TaskListType:
    id: uuid.UUID
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    tasks: list["TaskType"] | None


@sb.type
class TaskType:
    id: uuid.UUID
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
    todolist: TaskListType | None
    assignee: UserType | None


# Inputs for mutations
@sb.input
class TaskCreateInput:
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    tasklist_id: uuid.UUID
    assignee_id: uuid.UUID | None = None


@sb.input
class TaskUpdateInput:
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    tasklist_id: uuid.UUID | None = None
    assignee_id: uuid.UUID | None = None


@sb.input
class TaskListCreateInput:
    title: str
    description: str | None = None


@sb.input
class TaskListUpdateInput:
    title: str | None = None
    description: str | None = None
