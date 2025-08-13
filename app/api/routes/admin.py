from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import SessionDep
from app.api.dependencies.auth import authenticate_user, create_access_token
from app.core.exceptions.auth import UserNotFound
from app.crud.user import UserCRUD
from app.schemas.user import UserCreateBody, UserResponseBody

router = APIRouter()


@router.post("/token")
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise UserNotFound()

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "",
    summary="Create an user",
    response_description="Create a new user",
    status_code=HTTPStatus.CREATED,
)
async def api_create_user(
    create_user: UserCreateBody,
    session: SessionDep,
) -> UserResponseBody:
    user_crud = UserCRUD(session)
    user = await user_crud.new_user(create_user)
    return UserResponseBody(**user.model_dump(mode="json"))
