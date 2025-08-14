import uuid
from enum import Enum

from pydantic import ConfigDict, EmailStr
from sqlmodel import Field, Relationship

from app.models import BaseSQLModel


class UserTitle(str, Enum):
    Mr = "Mr"
    Ms = "Ms"
    X = "X"


class User(BaseSQLModel, table=True):
    """
    SQL model for user entity
    """

    __tablename__ = "users"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    title: UserTitle | None = Field(
        default=None,
        max_length=255,
        description="Title of the user",
    )
    first_name: str = Field(
        max_length=255,
        description="First name of the user",
    )

    last_name: str = Field(
        max_length=255,
        description="Last name of the user",
    )
    email: EmailStr = Field(description="", index=True, unique=True)

    hashed_password: str

    tasks: list["Task"] = Relationship(
        back_populates="assignee",
        sa_relationship_kwargs={"foreign_keys": "[Task.assignee_id]"},
    )  # type: ignore
