FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install uv

COPY uv.lock .
COPY pyproject.toml .

RUN uv sync

#--------------------
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]