from logging import getLogger

from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

from app.api.routes.admin import router as admin_router
from app.graphql.schemas import schema


logger = getLogger(__name__)

api_router = APIRouter()
api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])

graphql_app = GraphQLRouter(schema)
