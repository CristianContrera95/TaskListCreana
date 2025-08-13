from app.crud import AsyncCRUD
from app.models.tasklist import Task, TaskList
from app.schemas.tasklist import (
    TaskCreateBody,
    TaskListCreateBody,
    TaskListUpdateBody,
    TaskUpdateBody,
)


class TaskListCRUD(AsyncCRUD[TaskList, TaskListCreateBody, TaskListUpdateBody]):
    def __init__(self, session):
        super().__init__(Task, session)


class TaskCRUD(AsyncCRUD[Task, TaskCreateBody, TaskUpdateBody]):
    def __init__(self, session):
        super().__init__(Task, session)
