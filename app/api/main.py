from logging import getLogger

from fastapi import APIRouter

from app.api.routes.admin import router as admin_router

logger = getLogger(__name__)

api_router = APIRouter()
api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
