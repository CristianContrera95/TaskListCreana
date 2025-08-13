from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.dependencies.auth import UserDepends
from app.databases.database import get_async_session

__all__ = ["SessionDep", "UserDepends"]

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
