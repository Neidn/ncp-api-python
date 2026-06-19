# ncp-api-python Development Harness Design

**Date:** 2026-06-20  
**Status:** Approved

## Overview

Python library for NCP (Naver Cloud Platform) API. Distributed via GitHub URL (`uv add git+https://github.com/...@vX.Y.Z`). Solo developer workflow — no PR process, direct push to `main`.

## Project Structure

```
ncp-api-python/
├── src/
│   └── ncp_api/
│       └── __init__.py          # __version__ single source of truth
├── tests/
│   └── __init__.py
├── .github/
│   └── workflows/
│       └── main.yml             # single workflow: lint → test → release
├── docs/
│   └── superpowers/specs/
├── pyproject.toml
└── Makefile
```

## CI/CD Pipeline

Single workflow file: `.github/workflows/main.yml`

**Trigger:** push to `main`

**Jobs:**

```
lint ─┐
      ├─→ test (matrix) ─→ release
typecheck ─┘
```

1. **lint** — `ruff check .` + `ruff format --check .` (Python 3.12)
2. **typecheck** — `mypy src/` (Python 3.12)
   - `lint` + `typecheck` run in parallel
3. **test** — `needs: [lint, typecheck]`
   - Matrix: Python 3.9, 3.10, 3.11, 3.12
   - `uv sync --all-groups && pytest`

4. **release** — `needs: test`
   - `python-semantic-release`
   - Parses commits since last tag:
     - `fix:` → patch bump (0.1.0 → 0.1.1)
     - `feat:` → minor bump (0.1.0 → 0.2.0)
     - `BREAKING CHANGE` in footer → major bump (0.1.0 → 1.0.0)
     - `chore:` / `docs:` / `refactor:` → no release
   - On release: bumps `__version__` in `src/ncp_api/__init__.py`, bumps `version` in `pyproject.toml`, creates git tag `vX.Y.Z`, creates GitHub Release with auto-generated changelog
   - Requires: `GITHUB_TOKEN` with write permissions (provided by default in Actions)

## Tooling

### Dev Tools
- **ruff** — lint + format (replaces flake8 + black + isort)
- **mypy** — static type checking, strict mode
- **pytest** + **pytest-cov** — test runner + coverage

### pyproject.toml Configuration

```toml
[project]
name = "ncp-api-python"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = []

[dependency-groups]
dev = [
    "ruff",
    "mypy",
    "pytest",
    "pytest-cov",
    "python-semantic-release",
]

[tool.ruff]
target-version = "py39"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.mypy]
strict = true
python_version = "3.9"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.semantic_release]
version_variables = ["src/ncp_api/__init__.py:__version__"]
version_toml = ["pyproject.toml:project.version"]
branch = "main"
commit_message = "chore(release): v{version} [skip ci]"
```

### Makefile

```makefile
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
```

### src/ncp_api/__init__.py

```python
__version__ = "0.1.0"
```

## Usage After Setup

Install from GitHub:
```bash
uv add git+https://github.com/<org>/ncp-api-python
uv add git+https://github.com/<org>/ncp-api-python@v1.2.0
```

Local dev:
```bash
make dev      # install all deps
make check    # full local validation (lint + typecheck + test)
make format   # auto-fix formatting
```

## Constraints

- No PyPI publishing
- `GITHUB_TOKEN` only (no external secrets needed)
- `[skip ci]` in release commit message prevents infinite workflow loop
