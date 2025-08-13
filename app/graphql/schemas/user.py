
import strawberry as sb

from app.crud.user import UserCRUD
from app.databases.database import get_async_session
from app.graphql.types.user import UserType, TaskBasicType


@sb.type
class UserQuery:

    @sb.field
    async def get_user(self, user_id: sb.ID) -> UserType | None:
        async for session in get_async_session():
            crud = UserCRUD(session)
            user = await crud.get_by_id(str(user_id))
            if not user:
                return None  # TODO: raise better error

            tasks = list(user.tasks) if user.tasks is not None else []
            tasks_out = [
                TaskBasicType(
                    id=str(t.id),
                    title=t.title,
                ) for t in tasks
            ]

            return UserType(
                id=str(user.id),
                title=user.title,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                tasklist=tasks_out,
                created_at=user.created_at,
                updated_at=user.updated_at
            )

    @sb.field
    async def list_users(self) -> list[UserType] | None:
        result: list[UserType] = []
        async for session in get_async_session():
            crud = UserCRUD(session)
            users = await crud.get_list()

            if not users:
                return None  # TODO: raise better error

            for user in users:
                tasks = list(user.tasks) if user.tasks is not None else []
                tasks_out = [
                    TaskBasicType(
                        id=str(t.id),
                        title=t.title,
                    ) for t in tasks
                ]

                result.append(UserType(
                    id=str(user.id),
                    title=user.title,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    tasklist=tasks_out,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                ))
        return result

