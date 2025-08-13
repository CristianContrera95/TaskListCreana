from sqlmodel import col, select

from app.api.dependencies.auth import get_password_hash
from app.core.exceptions.auth import UserAlreadyExists
from app.crud import AsyncCRUD
from app.models.user import User
from app.schemas.user import UserCreateBody, UserUpdateBody


class UserCRUD(AsyncCRUD[User, UserCreateBody, UserUpdateBody]):
    def __init__(self, session):
        super().__init__(User, session)

    async def new_user(self, create_user: UserCreateBody) -> User:
        # validate email don't exists
        stmt = select(User).where(col(User.email) == create_user.email)
        curr_user = (await self.execute_stmt(stmt)).first()

        if curr_user:
            raise UserAlreadyExists(
                f"User with email {create_user.email} already exists"
            )

        # hash password
        setattr(
            create_user,
            "hashed_password",
            get_password_hash(create_user.hashed_password),
        )
        user = await self.create(create_user)
        return user
