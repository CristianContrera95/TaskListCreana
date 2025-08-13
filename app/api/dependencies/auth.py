import os
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlmodel import col
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions.auth import InvalidAccessToken
from app.models.user import User

SECRET_KEY = os.getenv("SECRET_KEY", "Hire me with a good salary please")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "300"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def get_password_hash(password):
    return pwd_context.hash(password)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise InvalidAccessToken()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(col(User.email) == email)
    result = await session.exec(stmt)
    return result.first()


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> User | None:
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not await verify_password(password, user.hashed_password):
        return None
    return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    data = decode_token(token)
    return User(**data)


UserDepends = Annotated[User, Depends(get_current_user)]
