import strawberry as sb

from app.graphql.schemas.tasklist import TaskListMutation, TaskListQuery
from app.graphql.schemas.user import UserQuery


@sb.type
class Query(UserQuery, TaskListQuery):
    pass


@sb.type
class Mutation(TaskListMutation):
    pass


schema = sb.Schema(query=Query, mutation=Mutation)
