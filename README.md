# TaskList Challenge for Creana

This project is the GraphQL version of the Todo challenge using:
- FastAPI
- Strawberry GraphQL
- SQLModel (async) + PostgreSQL

## Quickstart:
### Docker
1. Copy `.env` to root folder and set values.
2. Run with Docker Compose:
   ```bash
   docker compose up --build
   ```
3. Open GraphQL playground at `http://localhost:8000/graphql`.

### Local
0. Install uv and run:
   ```bash
   uv venv
   uv sync
   ```
1. Copy `.env` to root folder and set values.
2. Run with Docker Compose:
   ```bash
   make serve
   ```
3. Open GraphQL playground at `http://localhost:8000/graphql`.

### Test
0. Install uv and run:
   ```bash
   uv venv
   uv sync
   ```
1. Copy `.env` to root folder and set values.
2. Run with Docker Compose:
   ```bash
   make test
   ```
3. Open GraphQL playground at `http://localhost:8000/graphql`.

