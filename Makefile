.PHONY: serve format lint

serve:
	uv run uvicorn "app.main:app" --reload

format:
	uv run isort .
	uv run black .

lint:
	uv run flake8 app
	uv run pylint app
