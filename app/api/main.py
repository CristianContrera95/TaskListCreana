from logging import getLogger

from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

from app.api.routes.admin import router as admin_router
from app.graphql.auth import get_context
from app.graphql.schemas import schema


logger = getLogger(__name__)


### REST endpoints
rest_router = APIRouter()
rest_router.include_router(admin_router, prefix="/admin", tags=["Admin"])


### GraphQL endpoints
graphql_app = GraphQLRouter(schema, context_getter=get_context)