from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserTitle


class UserCreateBody(BaseModel):
    """
    Basic schema to create a new user
    """

    title: UserTitle | None = None
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str = Field(alias="password")


class UserUpdateBody(BaseModel):
    """
    Basic schema to update a new user
    """

    title: UserTitle | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserResponseBody(BaseModel):
    """
    Basic schema to response an user
    """

    title: UserTitle | None = None
    first_name: str
    last_name: str
    email: EmailStr
