# Dev Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up Python library dev harness with local tooling (ruff, mypy, pytest) and GitHub Actions CI/CD (lint → test matrix → auto semantic release on main push).

**Architecture:** Single `pyproject.toml` manages all tool config. One GitHub Actions workflow (`main.yml`) runs 4 jobs: lint and typecheck in parallel, test matrix (Python 3.9–3.12) after both pass, release via `python-semantic-release` after tests pass. Local dev uses `Makefile` wrappers around `uv run`.

**Tech Stack:** Python 3.9+, uv, ruff, mypy, pytest, python-semantic-release v9, GitHub Actions (astral-sh/setup-uv@v5, python-semantic-release/python-semantic-release@v9)

## Global Constraints

- Python: `>=3.9` (test matrix: 3.9, 3.10, 3.11, 3.12)
- Package manager: `uv` only (no pip, no poetry)
- Layout: `src/ncp_api/` (src-layout)
- `__version__` lives in `src/ncp_api/__init__.py` only
- No PyPI publishing — GitHub release only
- Conventional Commits required for auto-versioning
- Release commit message must contain `[skip ci]` to prevent loop

---

### Task 1: Project scaffold + pyproject.toml

**Files:**
- Modify: `pyproject.toml`
- Create: `src/ncp_api/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/test_package.py`

**Interfaces:**
- Produces: `ncp_api.__version__: str` — used by all downstream tasks to verify version

- [ ] **Step 1: Create src package**

```bash
mkdir -p src/ncp_api
```

Create `src/ncp_api/__init__.py`:

```python
__version__ = "0.1.0"
```

- [ ] **Step 2: Create tests package**

```bash
mkdir -p tests
touch tests/__init__.py
```

Create `tests/test_package.py`:

```python
import ncp_api


def test_version_exists():
    assert isinstance(ncp_api.__version__, str)


def test_version_format():
    parts = ncp_api.__version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
```

- [ ] **Step 3: Run test to verify it fails (package not importable yet)**

```bash
uv run pytest tests/test_package.py -v
```

Expected: `ModuleNotFoundError: No module named 'ncp_api'` — confirms src-layout not wired up yet.

- [ ] **Step 4: Update pyproject.toml**

Replace the entire file:

```toml
[project]
name = "ncp-api-python"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = []

[dependency-groups]
dev = [
    "ruff>=0.9.0",
    "mypy>=1.14.0",
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "python-semantic-release>=9.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/ncp_api"]

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

- [ ] **Step 5: Install deps and run tests**

```bash
uv sync --all-groups
uv run pytest tests/test_package.py -v
```

Expected output:
```
tests/test_package.py::test_version_exists PASSED
tests/test_package.py::test_version_format PASSED
2 passed in 0.XXs
```

- [ ] **Step 6: Verify ruff and mypy work**

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
```

Expected: all exit 0, no errors.

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml src/ tests/
git commit -m "feat: scaffold src-layout package with dev tooling config"
```

---

### Task 2: Makefile

**Files:**
- Create: `Makefile`

**Interfaces:**
- Consumes: `uv run ruff`, `uv run mypy`, `uv run pytest` (from Task 1)
- Produces: `make dev`, `make lint`, `make format`, `make typecheck`, `make test`, `make check`

- [ ] **Step 1: Create Makefile**

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

**Important:** Lines under each target MUST use a tab character (not spaces). If your editor converts tabs to spaces, check with `cat -A Makefile` — tab lines show as `^I`.

- [ ] **Step 2: Verify each target**

```bash
make lint
make typecheck
make test
make check
```

Expected: all exit 0.

- [ ] **Step 3: Commit**

```bash
git add Makefile
git commit -m "feat: add Makefile with dev shortcuts"
```

---

### Task 3: GitHub Actions workflow

**Files:**
- Create: `.github/workflows/main.yml`

**Interfaces:**
- Consumes: `uv sync --all-groups`, `ruff`, `mypy`, `pytest`, `semantic-release` (from Tasks 1–2)
- Produces: GitHub CI badges (lint, test), auto GitHub Releases on qualifying commits

- [ ] **Step 1: Create workflow directory**

```bash
mkdir -p .github/workflows
```

- [ ] **Step 2: Create .github/workflows/main.yml**

```yaml
name: CI/CD

on:
  push:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          python-version: "3.12"
      - run: uv sync --all-groups
      - run: uv run ruff check .
      - run: uv run ruff format --check .

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          python-version: "3.12"
      - run: uv sync --all-groups
      - run: uv run mypy src/

  test:
    needs: [lint, typecheck]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: uv sync --all-groups
      - run: uv run pytest

  release:
    needs: test
    runs-on: ubuntu-latest
    concurrency: release
    permissions:
      contents: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}
      - uses: astral-sh/setup-uv@v5
        with:
          python-version: "3.12"
      - run: uv sync --all-groups
      - uses: python-semantic-release/python-semantic-release@v9
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

- [ ] **Step 3: Verify YAML syntax**

```bash
uv run python -c "import yaml; yaml.safe_load(open('.github/workflows/main.yml'))"
```

Expected: no output (no error).

- [ ] **Step 4: Commit and push**

```bash
git add .github/
git commit -m "feat: add GitHub Actions CI/CD workflow"
git push origin main
```

- [ ] **Step 5: Verify CI on GitHub**

Go to `https://github.com/<your-org>/ncp-api-python/actions` and confirm:
- `lint` job: green
- `typecheck` job: green
- `test` job: 4 matrix runs (3.9, 3.10, 3.11, 3.12) — all green
- `release` job: green, but no release created (initial commit was `feat:` — check if v0.1.0 tag already exists; if not, a release should be created)

**Note:** If `release` job fails with permission error, go to repo Settings → Actions → General → Workflow permissions → set to "Read and write permissions".

---

## Post-Setup Verification

After all tasks complete, verify end-to-end:

```bash
# Local
make check

# Simulate conventional commit
git commit --allow-empty -m "fix: test auto-release"
git push origin main
# → CI runs → release job creates v0.1.1 tag + GitHub Release
```

Install via uv from GitHub:
```bash
uv add git+https://github.com/<your-org>/ncp-api-python@v0.1.0
```
