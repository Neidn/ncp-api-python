# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install all deps (runtime + dev)
make dev          # uv sync --all-groups

# Run everything (lint + typecheck + test)
make check

# Individual targets
make lint         # ruff check + format --check
make format       # ruff format (auto-fix)
make typecheck    # mypy src/
make test         # pytest (with coverage)

# Single test
uv run pytest tests/test_adapters_base.py::test_request_success -v
```

Package manager is `uv` — no pip, no poetry.

## Architecture

```
NcpClient (src/ncp_api/client.py)
  └── resolves env → PublicAdapter | GovAdapter | FinAdapter

PublicAdapter / GovAdapter / FinAdapter
  (src/ncp_api/adapters/{public,gov,fin}/__init__.py)
  └── inherit NcpHttpAdapter (src/ncp_api/adapters/base.py)
        ├── HmacSigner (src/ncp_api/auth.py)
        └── httpx.Client + httpx.AsyncClient

src/ncp_api/environment.py   — NcpEnv enum + BASE_URLS
src/ncp_api/exceptions.py    — NcpError hierarchy
```

**Adding a service API:**

1. Create `src/ncp_api/adapters/public/server.py` (or `gov/`, `fin/`)
2. Subclass `NcpHttpAdapter`, set class vars:
   ```python
   class ServerApi(NcpHttpAdapter):
       path_prefix: ClassVar[str] = "/vserver/v2"
       # _service_base_url: ClassVar[str] = "https://other.domain.com"  # only if service has its own domain
   ```
3. Wire into the environment adapter:
   ```python
   class PublicAdapter(NcpHttpAdapter):
       def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
           super().__init__(env_base_url, signer)
           self.server = ServerApi(env_base_url, signer)
   ```
4. Expose on `NcpClient` via `self._adapter.server`

**URL resolution:** `base_url + path_prefix + path`
- `base_url` = `_service_base_url` class var if set, else injected `env_base_url`
- HMAC signs path+query only (not full URL)

**Environments** (set via `env` param, `NCP_ENV` env var, or default `"public"`):
- `public` → `https://ncloud.apigw.ntruss.com`
- `gov` → `https://ncloud.apigw.gov-ntruss.com`
- `fin` → `https://ncloud.apigw.fin-ntruss.com`

## Key Conventions

- All source files use `from __future__ import annotations` for Python 3.9 compat with `|` union syntax
- Tests use `pytest-httpx` for HTTP mocking — no live network calls
- `asyncio_mode = "auto"` in pyproject.toml — no `@pytest.mark.asyncio` decorator needed
- Conventional Commits (`feat:`, `fix:`, `chore:`) → `python-semantic-release` auto-bumps version on push to `main`
- Errors from NCP: check `returnCode`/`returnMessage` first, fall back to `errorCode`/`message`

## CI/CD

GitHub Actions (`.github/workflows/main.yml`): lint → typecheck (parallel) → test (matrix 3.9–3.12) → release.
Release job runs `python-semantic-release` and publishes a GitHub Release with auto-generated tag.
