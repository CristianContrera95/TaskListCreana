import uuid

import strawberry as sb

from app.core.exceptions.database import NotFound
from app.core.exceptions.graphql import InvalidRequest
from app.core.utils import apply_filter
from app.crud.tasklist import TaskCRUD, TaskListCRUD
from app.crud.user import UserCRUD
from app.databases.database import get_async_session
from app.graphql.auth import Context, validate_auth_user
from app.graphql.types.tasklist import (
    TaskCreateInput,
    TaskListBasicType,
    TaskListCreateInput,
    TaskListType,
    TaskListUpdateInput,
    TaskType,
    TaskUpdateInput,
)
from app.graphql.types.user import UserType
from app.models.tasklist import TaskPriority, TaskStatus
from app.schemas.tasklist import (
    TaskCreateBody,
    TaskListCreateBody,
    TaskListUpdateBody,
    TaskUpdateBody,
)


@sb.type
class TaskListQuery:

    @sb.field
    async def get_tasklist(
        self,
        tasklist_id: sb.ID,
        status: list[TaskStatus] | None = None,
        priority: list[TaskPriority] | None = None,
    ) -> TaskListType | None:

        if not tasklist_id:
            raise InvalidRequest(f"Must specify a tasklist ID.")

        async for session in get_async_session():
            crud = TaskListCRUD(session)
            tasklist = await crud.get_by_id(str(tasklist_id))
            if not tasklist:
                return None

            tasks = list(tasklist.tasks) if tasklist.tasks is not None else []
            tasks_out = [
                TaskType(
                    id=str(t.id),
                    title=t.title,
                    description=t.description,
                    status=t.status,
                    priority=t.priority,
                    created_at=t.created_at,
                    updated_at=t.updated_at,
                    tasklist=TaskListBasicType(
                        id=str(tasklist.id), title=tasklist.title
                    ),
                    assignee=str(t.assignee_id) if t.assignee_id else None,
                )
                for t in tasks
                if (
                    apply_filter(str(t.status.value), status)
                    and apply_filter(str(t.priority.value), priority)
                )
            ]

            percent = (
                (
                    (
                        len(list(filter(lambda t: t.status == TaskStatus.done, tasks)))
                        / len(tasklist.tasks)
                    )
                    * 100
                )
                if tasks
                else 0
            )

            return TaskListType(
                id=str(tasklist.id),
                title=tasklist.title,
                description=tasklist.description,
                tasks=tasks_out,
                completion_percent=percent,
                updated_at=tasklist.updated_at,
                created_at=tasklist.created_at,
            )

    @sb.field
    async def list_tasklists(
        self,
        status: list[TaskStatus] | None = None,
        priority: list[TaskPriority] | None = None,
    ) -> list[TaskListType]:

        async def get_user(user_id: str) -> UserType | None:
            user_crud = UserCRUD(session)
            user = await user_crud.get_by_id(user_id)
            if user:
                return UserType(
                    **user.model_dump(
                        mode="json",
                        exclude={"hashed_password", "updated_by", "created_by"},
                    )
                )
            return None

        result: list[TaskListType] = []
        async for session in get_async_session():
            crud = TaskListCRUD(session)

            tasklists = await crud.get_list()

            for tasklist in tasklists:

                tasks = list(tasklist.tasks) if tasklist.tasks is not None else []

                percent = (
                    (
                        (
                            len(
                                list(
                                    filter(lambda t: t.status == TaskStatus.done, tasks)
                                )
                            )
                            / len(tasks)
                        )
                        * 100
                    )
                    if tasks
                    else 0
                )

                tasks_out = [
                    TaskType(
                        id=str(t.id),
                        title=t.title,
                        description=t.description,
                        status=t.status,
                        priority=t.priority,
                        created_at=t.created_at,
                        updated_at=t.updated_at,
                        tasklist=t.tasklist,
                        assignee=(
                            get_user(str(t.assignee_id)) if t.assignee_id else None
                        ),
                    )
                    for t in tasks
                    if (
                        apply_filter(str(t.status.value), status)
                        and apply_filter(str(t.priority.value), priority)
                    )
                ]

                result.append(
                    TaskListType(
                        id=str(tasklist.id),
                        title=tasklist.title,
                        description=tasklist.description,
                        tasks=tasks_out,
                        completion_percent=percent,
                        created_at=tasklist.created_at,
                        updated_at=tasklist.updated_at,
                    )
                )
        return result


@sb.type
class TaskListMutation:

    # -------- TaskList mutations --------
    @sb.mutation
    async def create_tasklist(
        self, data: TaskListCreateInput, info: sb.Info[Context]
    ) -> TaskListType | None:
        async for session in get_async_session():
            await validate_auth_user(session, info.context)
            crud = TaskListCRUD(session)
            created = await crud.create(
                TaskListCreateBody(title=data.title, description=data.description)
            )

            if not created:
                return None

            return TaskListType(
                id=created.id,
                title=created.title,
                description=created.description,
                created_at=created.created_at,
                updated_at=created.updated_at,
                tasks=[],
                completion_percent=0,
            )

    @sb.mutation
    async def update_tasklist(
        self, tasklist_id: uuid.UUID, data: TaskListUpdateInput, info: sb.Info[Context]
    ) -> TaskListType | None:

        if not tasklist_id:
            raise InvalidRequest(f"Must specify a tasklist ID.")

        async for session in get_async_session():
            await validate_auth_user(session, info.context)
            crud = TaskListCRUD(session)
            updated = await crud.update_by_id(
                tasklist_id,
                TaskListUpdateBody(title=data.title, description=data.description),
            )

            if not updated:
                return None

            tasks = list(updated.tasks) if updated.tasks else []

            tasks_out = [
                TaskType(
                    id=t.id,
                    title=t.title,
                    description=t.description,
                    status=t.status,
                    priority=t.priority,
                    created_at=t.created_at,
                    updated_at=t.updated_at,
                    assignee=t.assignee,
                )
                for t in tasks
            ]

            percent = (
                len([t for t in tasks if t.status == TaskStatus.done]) / len(tasks)
                if tasks
                else 0
            )

            return TaskListType(
                id=updated.id,
                title=updated.title,
                description=updated.description,
                created_at=updated.created_at,
                updated_at=updated.updated_at,
                tasks=tasks_out,
                completion_percent=percent,
            )

    @sb.mutation
    async def delete_tasklist(self, id_: str, info: sb.Info[Context]) -> bool:

        if not id_:
            raise InvalidRequest(f"Must specify a tasklist ID.")

        async for session in get_async_session():
            await validate_auth_user(session, info.context)
            crud = TaskListCRUD(session)
            r = await crud.delete_by_id(uuid.UUID(id_))

            if not r:
                raise NotFound(f"TaskList with id: {id_} not found")
            return r
        return False

    # -------- Task mutations --------
    @sb.mutation
    async def create_task(
        self, data: TaskCreateInput, info: sb.Info[Context]
    ) -> TaskType | None:
        async for session in get_async_session():
            await validate_auth_user(session, info.context)
            crud = TaskCRUD(session)
            created = await crud.create(
                TaskCreateBody(
                    title=data.title,
                    description=data.description,
                    status=data.status,
                    priority=data.priority,
                    tasklist_id=data.tasklist_id,
                )
            )

            if not created:
                return None

            return TaskType(
                id=created.id,
                title=created.title,
                description=created.description,
                status=created.status,
                priority=created.priority,
                created_at=created.created_at,
                updated_at=created.updated_at,
                tasklist=created.tasklist,
                assignee=created.assignee,
            )

    @sb.mutation
    async def update_task(
        self, task_id: uuid.UUID, data: TaskUpdateInput, info: sb.Info[Context]
    ) -> TaskType | None:

        if not task_id:
            raise InvalidRequest(f"Must specify a task ID.")

        async for session in get_async_session():
            await validate_auth_user(session, info.context)
            crud = TaskCRUD(session)
            updated = await crud.update_by_id(
                task_id,
                TaskUpdateBody(
                    title=data.title,
                    description=data.description,
                    status=data.status,
                    priority=data.priority,
                    assignee_id=data.assignee_id,
                ),
            )

            if not updated:
                return None

            return TaskType(
                id=updated.id,
                title=updated.title,
                description=updated.description,
                status=updated.status,
                priority=updated.priority,
                created_at=updated.created_at,
                updated_at=updated.updated_at,
                tasklist=updated.tasklist,
                assignee=updated.assignee,
            )

    @sb.mutation
    async def delete_task(self, id_: str, info: sb.Info[Context]) -> bool:

        if not id_:
            raise InvalidRequest(f"Must specify a task ID.")

        async for session in get_async_session():
            await validate_auth_user(session, info.context)
            crud = TaskCRUD(session)
            r = await crud.delete_by_id(uuid.UUID(id_))

            if not r:
                raise NotFound(f"Task with id: {id_} not found")
            return r
        return False
