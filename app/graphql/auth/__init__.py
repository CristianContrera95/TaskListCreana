import uuid

from fastapi import Depends, Request
from strawberry.fastapi.context import BaseContext

from app.api.dependencies.auth import get_current_user_from_token, oauth2_scheme
from app.core.exceptions.auth import InvalidAccessToken, UserNotFound
from app.crud.user import UserCRUD


class Context(BaseContext):
    def __init__(self, request: Request, user_id: uuid.UUID | None):
        self.request = request
        self.user_id = user_id
        super().__init__()


async def context_dependency(request: Request) -> Context:
    token = None
    user_id = None
    try:
        token = await oauth2_scheme(request)
        user_id = get_current_user_from_token(token)
    except Exception:
        pass

    return Context(request=request, user_id=user_id)


async def get_context(
    custom_context=Depends(context_dependency),
):
    return custom_context


async def validate_auth_user(session, context: Context):
    if not context.user_id:
        raise InvalidAccessToken("Authentication required to access this field.")
    crud = UserCRUD(session)
    curr_user = await crud.get_by_id(str(context.user_id))
    if not curr_user:
        raise UserNotFound()
