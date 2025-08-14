# TaskList Challenge for Creana

This project is the GraphQL version of the Todo challenge using:
- FastAPI
- Strawberry GraphQL
- SQLModel (async) + PostgreSQL

## Quickstart:
### Docker
1. Copy `.env` to root folder and set values.  
   - Nota: Check enviroment variable POSTGRES_SERVER is set to use with Docker
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
   - Nota: Check enviroment variable POSTGRES_SERVER is set to use with localhost
2. Set Up local PostGrestDB look at script folder
3. Run with Serve:
   ```bash
   make serve
   ```
4. Open GraphQL playground at `http://localhost:8000/graphql`.

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

---

Developers:

To contribute to this project, use a new branch for each feature o bugfix and do the pre-commits by your self, 
we trust in you!!! don't forget that!! 
```bash
   make format
   make lint
   git add .
   git commit -m "here your aport"
```
