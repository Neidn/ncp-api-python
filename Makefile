.PHONY: dev lint format typecheck test check

dev:
	uv sync --all-groups

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src/

test:
	uv run pytest

check: lint typecheck test
