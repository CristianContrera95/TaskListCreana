import uuid

import pytest


# ------------------------------------------------------
# GraphQL Queries Tests
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_list_tasklists(test_client):
    """Should return a list of tasklists without authentication."""
    query = """
    query {
        listTasklists {
            id
            title
        }
    }
    """
    resp = await test_client.post("/graphql", json={"query": query})
    assert resp.status_code == 200
    data = resp.json()["data"]["listTasklists"]
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_authenticated_user(test_client, auth_token):
    """Should return the authenticated user data when token is provided."""
    query = """
    query {
        getAuthenticatedUser {
            id
            lastName
            email
        }
    }
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = await test_client.post("/graphql", json={"query": query}, headers=headers)
    assert resp.status_code == 200

    response_json = resp.json()
    assert (
        "errors" not in response_json
    ), f"GraphQL errors found: {response_json.get('errors')}"

    data = response_json["data"]["getAuthenticatedUser"]
    assert data["email"] == "pepe@lui.com"


# ------------------------------------------------------
# GraphQL Mutations Tests (require authentication)
# ------------------------------------------------------
@pytest.mark.asyncio
async def test_create_tasklist(test_client, auth_token):
    """Should create a new tasklist when authenticated."""
    mutation = """
    mutation($data: TaskListCreateInput!) {
        createTasklist(data: $data) {
            id
            title
        }
    }
    """
    variables = {"data": {"title": "New List", "description": "A new task list"}}
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = await test_client.post(
        "/graphql", json={"query": mutation, "variables": variables}, headers=headers
    )
    assert resp.status_code == 200

    response_json = resp.json()
    assert (
        "errors" not in response_json
    ), f"GraphQL errors found: {response_json.get('errors')}"

    data = response_json["data"]["createTasklist"]
    assert data["title"] == "New List"


@pytest.mark.asyncio
async def test_update_tasklist(test_client, auth_token, created_tasklist_id):
    """Should update an existing tasklist."""
    mutation = """
    mutation($tasklistId: UUID!, $data: TaskListUpdateInput!) {
        updateTasklist(tasklistId: $tasklistId, data: $data) {
            id
            title
        }
    }
    """
    variables = {"tasklistId": created_tasklist_id, "data": {"title": "Other List"}}
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = await test_client.post(
        "/graphql", json={"query": mutation, "variables": variables}, headers=headers
    )
    assert resp.status_code == 200

    response_json = resp.json()
    assert (
        "errors" not in response_json
    ), f"GraphQL errors found: {response_json.get('errors')}"

    data = response_json["data"]["updateTasklist"]
    assert data["title"] == "Other List"


@pytest.mark.asyncio
async def test_delete_tasklist(test_client, auth_token, created_tasklist_id):
    """Should delete an existing tasklist."""
    mutation = """
    mutation($id_: String!) {
        deleteTasklist(id_: $id_)
    }
    """
    variables = {"id_": created_tasklist_id}
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = await test_client.post(
        "/graphql", json={"query": mutation, "variables": variables}, headers=headers
    )
    assert resp.status_code == 200

    response_json = resp.json()
    assert (
        "errors" not in response_json
    ), f"GraphQL errors found: {response_json.get('errors')}"

    data = response_json["data"]["deleteTasklist"]
    assert data is True
