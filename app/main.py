from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.main import api_router, graphql_app
from app.core.settings import settings
from app.databases.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="TaskListAPI", lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/check")
async def check():
    return {"ok": True}
