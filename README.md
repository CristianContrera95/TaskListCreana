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


## Usage
At `http://localhost:8000/docs` you'll find Swagger REST-API with two endpoint :

1. `POST /api/v1/admin` to create a new user to login at API.  
   - CURL example
```bash
   curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/admin' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Mr",
  "first_name": "pepe",
  "last_name": "lui",
  "email": "pepe@lui.com",
  "password": "strong"
}'
```

2. `POST /api/v1/admin/token` to generate a new token using email and password  
   - CURL example:
```bash
  curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/admin/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=pepe%40lui.com&password=strong&scope=&client_id=string&client_secret=********'
```

3. With your token like this:
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOi....j6_bw",
  "token_type": "bearer"
}
```
Go to `http://localhost:8000/graphql` and set authorization headers at the bottom of the web page
```
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOi....j6_bw"
}
```
4. Now yo can make any Query or Mutation. Without Authentication only can try Query Endpoints
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
