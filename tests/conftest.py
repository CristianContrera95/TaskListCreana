import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import SQLModel

# Set in-memory DB BEFORE importing app
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.databases.database import async_engine as engine
from app.main import app


# ------------------------------------------------------
# Async HTTP client
# ------------------------------------------------------
@pytest_asyncio.fixture(scope="session")
async def test_client():
    """Provides a reusable AsyncClient for the API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ------------------------------------------------------
# Reset DB before each test
# ------------------------------------------------------
@pytest_asyncio.fixture(autouse=True)
async def reset_db():
    """Drops and recreates all tables before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


# ------------------------------------------------------
# Auth token fixture
# ------------------------------------------------------
@pytest_asyncio.fixture
async def auth_token(test_client):
    """Creates a test user and retrieves a JWT token."""
    user_data = {
        "title": "Mr",
        "first_name": "pepe",
        "last_name": "lui",
        "email": "pepe@lui.com",
        "password": "test1234",
    }
    resp_create = await test_client.post("/api/v1/admin", json=user_data)
    assert resp_create.status_code in (
        200,
        201,
    ), f"User creation failed: {resp_create.text}"

    login_data = {"username": "pepe@lui.com", "password": "test1234"}
    resp_login = await test_client.post("/api/v1/admin/token", data=login_data)
    assert resp_login.status_code == 200, f"Login failed: {resp_login.text}"

    token = resp_login.json().get("access_token")
    assert token, f"Login did not return a token: {resp_login.json()}"
    return token


# ------------------------------------------------------
# TaskList creation fixture
# ------------------------------------------------------
@pytest_asyncio.fixture
async def created_tasklist_id(test_client, auth_token):
    """Creates a TaskList via GraphQL mutation."""
    mutation = """
    mutation CreateTaskList($data: TaskListCreateInput!) {
        createTasklist(data: $data) {
            id
            title
        }
    }
    """
    variables = {"data": {"title": "TaskList 1", "description": "A task list"}}
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = await test_client.post(
        "/graphql", json={"query": mutation, "variables": variables}, headers=headers
    )

    # Assert HTTP status code is 200
    assert (
        resp.status_code == 200
    ), f"HTTP request failed with status: {resp.status_code}"

    # Get the JSON response
    response_data = resp.json()

    # Check for and report GraphQL errors
    assert (
        "errors" not in response_data
    ), f"GraphQL errors: {response_data.get('errors')}"

    # Safely return the data
    return response_data["data"]["createTasklist"]["id"]
