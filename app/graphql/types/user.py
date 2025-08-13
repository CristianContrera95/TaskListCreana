import uuid
from datetime import datetime

import strawberry

from app.models.user import UserTitle


@strawberry.type
class UserType:
    id: uuid.UUID
    title: UserTitle | None
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime


@strawberry.input
class UserCreateInput:
    title: UserTitle | None
    first_name: str
    last_name: str
    email: str


@strawberry.input
class UserUpdateInput:
    title: UserTitle | None
    first_name: str | None
    last_name: str | None
    email: str | None
