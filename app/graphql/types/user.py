import uuid
from datetime import datetime

import strawberry as sb

from app.models.user import UserTitle


@sb.type
class TaskBasicType:
    id: uuid.UUID
    title: str


@sb.type
class UserType:
    id: uuid.UUID
    title: UserTitle | None
    first_name: str
    last_name: str
    email: str
    tasklist: list[TaskBasicType] | None
    created_at: datetime
    updated_at: datetime


@sb.input
class UserCreateInput:
    title: UserTitle | None
    first_name: str
    last_name: str
    email: str


@sb.input
class UserUpdateInput:
    title: UserTitle | None
    first_name: str | None
    last_name: str | None
    email: str | None
