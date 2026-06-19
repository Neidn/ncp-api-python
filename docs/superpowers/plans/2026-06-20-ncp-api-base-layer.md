# NCP API Base Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the NCP API Python client base layer: HMAC auth, environment config, HTTP adapter, error types, and empty adapter scaffolding for Public/Gov/Fin environments.

**Architecture:** `NcpClient` resolves environment (param > `NCP_ENV` env var > "public") and instantiates the matching adapter (`PublicAdapter` / `GovAdapter` / `FinAdapter`), all of which inherit `NcpHttpAdapter`. The HTTP adapter holds an `HmacSigner` and two httpx clients (sync + async). Services override `_service_base_url` (ClassVar) and `path_prefix` to customize URL resolution without touching HTTP logic.

**Tech Stack:** Python 3.9+, httpx>=0.27.0 (runtime), pytest-httpx>=0.30.0 (test), ruff, mypy strict

## Global Constraints

- Python: `>=3.9` — no `X | Y` union syntax, use `Union[X, Y]` or `Optional[X]`; no `str | None` in runtime code (annotations only with `from __future__ import annotations`)
- Package manager: `uv` only
- Layout: `src/ncp_api/`
- mypy strict — all public functions must have complete type annotations
- httpx `>=0.27.0` only runtime dependency
- Conventional Commits for all git commits
- NCP HMAC signature string format: `"{METHOD}\n{URL_PATH_AND_QUERY}\n{TIMESTAMP}\n{ACCESS_KEY}"`
- Auth headers: `x-ncp-apigw-timestamp`, `x-ncp-iam-access-key`, `x-ncp-apigw-signature-v2`

---

### Task 1: Exceptions + Environment + Dependencies

**Files:**
- Modify: `pyproject.toml`
- Create: `src/ncp_api/exceptions.py`
- Create: `src/ncp_api/environment.py`
- Test: `tests/test_exceptions.py`
- Test: `tests/test_environment.py`

**Interfaces:**
- Produces:
  - `NcpError(Exception)` — base exception
  - `NcpAuthError(NcpError)` — 401 / signature failure
  - `NcpApiError(NcpError)` — non-2xx API response; attrs: `status_code: int`, `error_code: str`, `message: str`
  - `NcpNetworkError(NcpError)` — connection/timeout failure
  - `NcpEnv(str, Enum)` — values: `"public"`, `"gov"`, `"fin"`
  - `BASE_URLS: dict[NcpEnv, str]` — env → base URL mapping

- [ ] **Step 1: Write failing tests**

Create `tests/test_exceptions.py`:

```python
from __future__ import annotations

import pytest

from ncp_api.exceptions import NcpApiError, NcpAuthError, NcpError, NcpNetworkError


def test_ncp_error_is_exception() -> None:
    assert issubclass(NcpError, Exception)


def test_ncp_auth_error_is_ncp_error() -> None:
    assert issubclass(NcpAuthError, NcpError)


def test_ncp_network_error_is_ncp_error() -> None:
    assert issubclass(NcpNetworkError, NcpError)


def test_ncp_api_error_is_ncp_error() -> None:
    assert issubclass(NcpApiError, NcpError)


def test_ncp_api_error_has_attrs() -> None:
    err = NcpApiError(status_code=400, error_code="1001", message="bad request")
    assert err.status_code == 400
    assert err.error_code == "1001"
    assert err.message == "bad request"
    assert str(err) == "bad request"


def test_ncp_api_error_inherits_message() -> None:
    err = NcpApiError(status_code=500, error_code="9999", message="server error")
    with pytest.raises(NcpError):
        raise err
```

Create `tests/test_environment.py`:

```python
from __future__ import annotations

import pytest

from ncp_api.environment import BASE_URLS, NcpEnv


def test_ncp_env_values() -> None:
    assert NcpEnv.PUBLIC == "public"
    assert NcpEnv.GOV == "gov"
    assert NcpEnv.FIN == "fin"


def test_ncp_env_from_string() -> None:
    assert NcpEnv("public") is NcpEnv.PUBLIC
    assert NcpEnv("gov") is NcpEnv.GOV
    assert NcpEnv("fin") is NcpEnv.FIN


def test_ncp_env_invalid_raises() -> None:
    with pytest.raises(ValueError):
        NcpEnv("invalid")


def test_base_urls_keys() -> None:
    assert set(BASE_URLS.keys()) == {NcpEnv.PUBLIC, NcpEnv.GOV, NcpEnv.FIN}


def test_base_urls_public() -> None:
    assert BASE_URLS[NcpEnv.PUBLIC] == "https://ncloud.apigw.ntruss.com"


def test_base_urls_gov() -> None:
    assert BASE_URLS[NcpEnv.GOV] == "https://ncloud.apigw.gov-ntruss.com"


def test_base_urls_fin() -> None:
    assert BASE_URLS[NcpEnv.FIN] == "https://ncloud.apigw.fin-ntruss.com"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_exceptions.py tests/test_environment.py -v
```

Expected: `ModuleNotFoundError: No module named 'ncp_api.exceptions'`

- [ ] **Step 3: Update pyproject.toml**

Add `httpx` as runtime dependency and `pytest-httpx` as dev dependency:

```toml
[project]
name = "ncp-api-python"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = ["httpx>=0.27.0"]

[dependency-groups]
dev = [
    "ruff>=0.9.0",
    "mypy>=1.14.0",
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "pytest-httpx>=0.30.0",
    "pytest-asyncio>=0.24.0",
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
pythonpath = ["src"]
addopts = "--cov=ncp_api --cov-report=term-missing"
asyncio_mode = "auto"

[tool.semantic_release]
version_variables = ["src/ncp_api/__init__.py:__version__"]
version_toml = ["pyproject.toml:project.version"]
branch = "main"
commit_message = "chore(release): v{version} [skip ci]"
```

- [ ] **Step 4: Create exceptions.py**

Create `src/ncp_api/exceptions.py`:

```python
from __future__ import annotations


class NcpError(Exception):
    """Base exception for all NCP API errors."""


class NcpAuthError(NcpError):
    """Raised on 401 responses or HMAC signature failures."""


class NcpApiError(NcpError):
    """Raised on non-2xx API responses."""

    def __init__(self, *, status_code: int, error_code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message


class NcpNetworkError(NcpError):
    """Raised on connection failures or timeouts."""
```

- [ ] **Step 5: Create environment.py**

Create `src/ncp_api/environment.py`:

```python
from __future__ import annotations

from enum import Enum


class NcpEnv(str, Enum):
    PUBLIC = "public"
    GOV = "gov"
    FIN = "fin"


BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://ncloud.apigw.ntruss.com",
    NcpEnv.GOV: "https://ncloud.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://ncloud.apigw.fin-ntruss.com",
}
```

- [ ] **Step 6: Sync deps and run tests**

```bash
uv sync --all-groups
uv run pytest tests/test_exceptions.py tests/test_environment.py -v
```

Expected:
```
tests/test_exceptions.py::test_ncp_error_is_exception PASSED
tests/test_exceptions.py::test_ncp_auth_error_is_ncp_error PASSED
tests/test_exceptions.py::test_ncp_network_error_is_ncp_error PASSED
tests/test_exceptions.py::test_ncp_api_error_is_ncp_error PASSED
tests/test_exceptions.py::test_ncp_api_error_has_attrs PASSED
tests/test_exceptions.py::test_ncp_api_error_inherits_message PASSED
tests/test_environment.py::test_ncp_env_values PASSED
tests/test_environment.py::test_ncp_env_from_string PASSED
tests/test_environment.py::test_ncp_env_invalid_raises PASSED
tests/test_environment.py::test_base_urls_keys PASSED
tests/test_environment.py::test_base_urls_public PASSED
tests/test_environment.py::test_base_urls_gov PASSED
tests/test_environment.py::test_base_urls_fin PASSED
13 passed
```

- [ ] **Step 7: Verify mypy and ruff**

```bash
uv run mypy src/
uv run ruff check .
```

Expected: both exit 0.

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml src/ncp_api/exceptions.py src/ncp_api/environment.py tests/test_exceptions.py tests/test_environment.py
git commit -m "feat: add exception hierarchy and environment config"
```

---

### Task 2: HmacSigner

**Files:**
- Create: `src/ncp_api/auth.py`
- Test: `tests/test_auth.py`

**Interfaces:**
- Consumes: nothing (stdlib only: `base64`, `hashlib`, `hmac`)
- Produces:
  - `HmacSigner(access_key: str, secret_key: str)`
  - `HmacSigner.sign(method: str, url: str, timestamp: int) -> dict[str, str]`
    - `method`: HTTP method uppercase, e.g. `"GET"`
    - `url`: path + query string only, e.g. `"/vserver/v2/getServerInstanceList?regionCode=KR"`
    - `timestamp`: Unix milliseconds as int
    - Returns: `{"x-ncp-apigw-timestamp": str, "x-ncp-iam-access-key": str, "x-ncp-apigw-signature-v2": str}`

- [ ] **Step 1: Write failing tests**

Create `tests/test_auth.py`:

```python
from __future__ import annotations

import base64
import hashlib
import hmac as stdlib_hmac


from ncp_api.auth import HmacSigner


def _expected_signature(secret_key: str, method: str, url: str, timestamp: int, access_key: str) -> str:
    string_to_sign = f"{method}\n{url}\n{timestamp}\n{access_key}"
    mac = stdlib_hmac.new(
        secret_key.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    )
    return base64.b64encode(mac.digest()).decode("utf-8")


def test_sign_returns_all_three_headers() -> None:
    signer = HmacSigner("testkey", "testsecret")
    headers = signer.sign("GET", "/test/path", 1700000000000)
    assert set(headers.keys()) == {
        "x-ncp-apigw-timestamp",
        "x-ncp-iam-access-key",
        "x-ncp-apigw-signature-v2",
    }


def test_sign_timestamp_header() -> None:
    signer = HmacSigner("testkey", "testsecret")
    headers = signer.sign("GET", "/test/path", 1700000000000)
    assert headers["x-ncp-apigw-timestamp"] == "1700000000000"


def test_sign_access_key_header() -> None:
    signer = HmacSigner("mykey", "mysecret")
    headers = signer.sign("GET", "/test/path", 1700000000000)
    assert headers["x-ncp-iam-access-key"] == "mykey"


def test_sign_signature_matches_hmac_sha256() -> None:
    access_key = "testkey"
    secret_key = "testsecret"
    timestamp = 1700000000000
    method = "GET"
    url = "/vserver/v2/getServerInstanceList"

    signer = HmacSigner(access_key, secret_key)
    headers = signer.sign(method, url, timestamp)

    expected = _expected_signature(secret_key, method, url, timestamp, access_key)
    assert headers["x-ncp-apigw-signature-v2"] == expected


def test_sign_different_methods_produce_different_signatures() -> None:
    signer = HmacSigner("key", "secret")
    get_sig = signer.sign("GET", "/path", 1000)["x-ncp-apigw-signature-v2"]
    post_sig = signer.sign("POST", "/path", 1000)["x-ncp-apigw-signature-v2"]
    assert get_sig != post_sig


def test_sign_different_urls_produce_different_signatures() -> None:
    signer = HmacSigner("key", "secret")
    sig_a = signer.sign("GET", "/path/a", 1000)["x-ncp-apigw-signature-v2"]
    sig_b = signer.sign("GET", "/path/b", 1000)["x-ncp-apigw-signature-v2"]
    assert sig_a != sig_b


def test_sign_query_string_included_in_signature() -> None:
    signer = HmacSigner("key", "secret")
    sig_no_query = signer.sign("GET", "/path", 1000)["x-ncp-apigw-signature-v2"]
    sig_with_query = signer.sign("GET", "/path?foo=bar", 1000)["x-ncp-apigw-signature-v2"]
    assert sig_no_query != sig_with_query
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_auth.py -v
```

Expected: `ModuleNotFoundError: No module named 'ncp_api.auth'`

- [ ] **Step 3: Implement HmacSigner**

Create `src/ncp_api/auth.py`:

```python
from __future__ import annotations

import base64
import hashlib
import hmac


class HmacSigner:
    def __init__(self, access_key: str, secret_key: str) -> None:
        self._access_key = access_key
        self._secret_key = secret_key

    def sign(self, method: str, url: str, timestamp: int) -> dict[str, str]:
        """Return NCP HMAC-SHA256 auth headers for one request.

        Args:
            method: HTTP method in uppercase, e.g. "GET".
            url: Path + query string only, e.g. "/vserver/v2/list?region=KR".
            timestamp: Unix time in milliseconds.
        """
        string_to_sign = f"{method}\n{url}\n{timestamp}\n{self._access_key}"
        mac = hmac.new(
            self._secret_key.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha256,
        )
        signature = base64.b64encode(mac.digest()).decode("utf-8")
        return {
            "x-ncp-apigw-timestamp": str(timestamp),
            "x-ncp-iam-access-key": self._access_key,
            "x-ncp-apigw-signature-v2": signature,
        }
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_auth.py -v
```

Expected: 7 passed.

- [ ] **Step 5: Verify mypy and ruff**

```bash
uv run mypy src/ncp_api/auth.py
uv run ruff check src/ncp_api/auth.py
```

Expected: both exit 0.

- [ ] **Step 6: Commit**

```bash
git add src/ncp_api/auth.py tests/test_auth.py
git commit -m "feat: add HmacSigner for NCP HMAC-SHA256 authentication"
```

---

### Task 3: NcpHttpAdapter

**Files:**
- Create: `src/ncp_api/adapters/__init__.py`
- Create: `src/ncp_api/adapters/base.py`
- Test: `tests/test_adapters_base.py`

**Interfaces:**
- Consumes:
  - `HmacSigner(access_key: str, secret_key: str)` — from Task 2
  - `NcpAuthError`, `NcpApiError`, `NcpNetworkError` — from Task 1
- Produces:
  - `NcpHttpAdapter(env_base_url: str, signer: HmacSigner)`
  - `NcpHttpAdapter.path_prefix: ClassVar[str] = ""`
  - `NcpHttpAdapter._service_base_url: ClassVar[Optional[str]] = None`
  - `NcpHttpAdapter.base_url: str` (property — returns `_service_base_url or _env_base_url`)
  - `NcpHttpAdapter.request(method: str, path: str, **kwargs: Any) -> dict[str, Any]`
  - `NcpHttpAdapter.arequest(method: str, path: str, **kwargs: Any) -> dict[str, Any]` (async)

- [ ] **Step 1: Write failing tests**

Create `tests/test_adapters_base.py`:

```python
from __future__ import annotations

from typing import Any

import httpx
import pytest

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.auth import HmacSigner
from ncp_api.exceptions import NcpApiError, NcpAuthError, NcpNetworkError


def make_adapter(base_url: str = "https://ncloud.apigw.ntruss.com") -> NcpHttpAdapter:
    signer = HmacSigner("testkey", "testsecret")
    return NcpHttpAdapter(base_url, signer)


def test_base_url_uses_env_url_when_no_service_override() -> None:
    adapter = make_adapter("https://example.com")
    assert adapter.base_url == "https://example.com"


def test_service_base_url_override() -> None:
    class ServiceWithOwnDomain(NcpHttpAdapter):
        _service_base_url = "https://kr.object.ncloudstorage.com"

    signer = HmacSigner("k", "s")
    service = ServiceWithOwnDomain("https://ncloud.apigw.ntruss.com", signer)
    assert service.base_url == "https://kr.object.ncloudstorage.com"


def test_path_prefix_default_empty() -> None:
    adapter = make_adapter()
    assert adapter.path_prefix == ""


def test_path_prefix_combined_in_resolve() -> None:
    class ServerApi(NcpHttpAdapter):
        path_prefix = "/vserver/v2"

    signer = HmacSigner("k", "s")
    api = ServerApi("https://ncloud.apigw.ntruss.com", signer)
    assert api._resolve_url("/getServerInstanceList") == (
        "https://ncloud.apigw.ntruss.com/vserver/v2/getServerInstanceList"
    )


def test_request_success(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"returnCode": "0", "data": "ok"})
    adapter = make_adapter()
    result = adapter.request("GET", "/test/path")
    assert result == {"returnCode": "0", "data": "ok"}


def test_request_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={})
    adapter = make_adapter()
    adapter.request("GET", "/test/path")
    sent_request = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent_request.headers
    assert "x-ncp-iam-access-key" in sent_request.headers
    assert "x-ncp-apigw-signature-v2" in sent_request.headers


def test_request_401_raises_auth_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(status_code=401, json={"returnCode": "401", "returnMessage": "Unauthorized"})
    adapter = make_adapter()
    with pytest.raises(NcpAuthError):
        adapter.request("GET", "/test/path")


def test_request_4xx_raises_api_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        status_code=400,
        json={"returnCode": "1001", "returnMessage": "Invalid parameter"},
    )
    adapter = make_adapter()
    with pytest.raises(NcpApiError) as exc_info:
        adapter.request("GET", "/test/path")
    assert exc_info.value.status_code == 400
    assert exc_info.value.error_code == "1001"
    assert exc_info.value.message == "Invalid parameter"


def test_request_5xx_raises_api_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        status_code=500,
        json={"returnCode": "9999", "returnMessage": "Internal error"},
    )
    adapter = make_adapter()
    with pytest.raises(NcpApiError) as exc_info:
        adapter.request("GET", "/test/path")
    assert exc_info.value.status_code == 500


def test_request_network_error_raises_network_error(httpx_mock: Any) -> None:
    httpx_mock.add_exception(httpx.ConnectError("connection refused"))
    adapter = make_adapter()
    with pytest.raises(NcpNetworkError):
        adapter.request("GET", "/test/path")


def test_request_timeout_raises_network_error(httpx_mock: Any) -> None:
    httpx_mock.add_exception(httpx.TimeoutException("timed out"))
    adapter = make_adapter()
    with pytest.raises(NcpNetworkError):
        adapter.request("GET", "/test/path")


@pytest.mark.asyncio
async def test_arequest_success(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"returnCode": "0"})
    adapter = make_adapter()
    result = await adapter.arequest("GET", "/test/path")
    assert result == {"returnCode": "0"}


@pytest.mark.asyncio
async def test_arequest_401_raises_auth_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(status_code=401, json={})
    adapter = make_adapter()
    with pytest.raises(NcpAuthError):
        await adapter.arequest("GET", "/test/path")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_adapters_base.py -v
```

Expected: `ModuleNotFoundError: No module named 'ncp_api.adapters'`

- [ ] **Step 3: Create adapters/__init__.py**

Create `src/ncp_api/adapters/__init__.py` (empty):

```python
```

- [ ] **Step 4: Implement NcpHttpAdapter**

Create `src/ncp_api/adapters/base.py`:

```python
from __future__ import annotations

import time
from typing import Any, ClassVar, Optional

import httpx

from ncp_api.auth import HmacSigner
from ncp_api.exceptions import NcpApiError, NcpAuthError, NcpNetworkError


class NcpHttpAdapter:
    path_prefix: ClassVar[str] = ""
    _service_base_url: ClassVar[Optional[str]] = None

    def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
        self._env_base_url = env_base_url
        self._signer = signer
        self._client = httpx.Client()
        self._async_client = httpx.AsyncClient()

    @property
    def base_url(self) -> str:
        return self._service_base_url or self._env_base_url

    def _resolve_url(self, path: str) -> str:
        return f"{self.base_url}{self.path_prefix}{path}"

    def _make_auth_headers(self, method: str, url: str) -> dict[str, str]:
        parsed = httpx.URL(url)
        sign_target = parsed.path
        if parsed.query:
            sign_target = f"{parsed.path}?{parsed.query}"
        timestamp = int(time.time() * 1000)
        return self._signer.sign(method.upper(), sign_target, timestamp)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        if response.status_code == 401:
            raise NcpAuthError(f"Authentication failed ({response.status_code})")
        if response.is_error:
            try:
                body: dict[str, Any] = response.json()
            except Exception:
                body = {}
            error_code = str(
                body.get("returnCode", body.get("errorCode", str(response.status_code)))
            )
            message = str(
                body.get("returnMessage", body.get("message", response.text))
            )
            raise NcpApiError(
                status_code=response.status_code,
                error_code=error_code,
                message=message,
            )
        result: dict[str, Any] = response.json()
        return result

    def request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._resolve_url(path)
        auth_headers = self._make_auth_headers(method, url)
        try:
            response = self._client.request(
                method=method.upper(),
                url=url,
                headers=auth_headers,
                **kwargs,
            )
            return self._handle_response(response)
        except (NcpAuthError, NcpApiError):
            raise
        except httpx.ConnectError as exc:
            raise NcpNetworkError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise NcpNetworkError(str(exc)) from exc

    async def arequest(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._resolve_url(path)
        auth_headers = self._make_auth_headers(method, url)
        try:
            response = await self._async_client.request(
                method=method.upper(),
                url=url,
                headers=auth_headers,
                **kwargs,
            )
            return self._handle_response(response)
        except (NcpAuthError, NcpApiError):
            raise
        except httpx.ConnectError as exc:
            raise NcpNetworkError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise NcpNetworkError(str(exc)) from exc
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
uv run pytest tests/test_adapters_base.py -v
```

Expected: 14 passed.

- [ ] **Step 6: Verify mypy and ruff**

```bash
uv run mypy src/ncp_api/adapters/
uv run ruff check src/ncp_api/adapters/
```

Expected: both exit 0.

- [ ] **Step 7: Commit**

```bash
git add src/ncp_api/adapters/ tests/test_adapters_base.py
git commit -m "feat: add NcpHttpAdapter with HMAC auth and error mapping"
```

---

### Task 4: Adapter Scaffolding + NcpClient + Public __init__.py

**Files:**
- Create: `src/ncp_api/adapters/public/__init__.py`
- Create: `src/ncp_api/adapters/gov/__init__.py`
- Create: `src/ncp_api/adapters/fin/__init__.py`
- Create: `src/ncp_api/client.py`
- Modify: `src/ncp_api/__init__.py`
- Test: `tests/test_client.py`

**Interfaces:**
- Consumes:
  - `NcpHttpAdapter(env_base_url: str, signer: HmacSigner)` — Task 3
  - `HmacSigner(access_key: str, secret_key: str)` — Task 2
  - `NcpEnv`, `BASE_URLS` — Task 1
  - `NcpError`, `NcpAuthError`, `NcpApiError`, `NcpNetworkError` — Task 1
- Produces:
  - `PublicAdapter(NcpHttpAdapter)` — empty, for Public cloud
  - `GovAdapter(NcpHttpAdapter)` — empty, for Gov cloud
  - `FinAdapter(NcpHttpAdapter)` — empty, for Fin cloud
  - `NcpClient(access_key: str, secret_key: str, env: str | NcpEnv | None = None)`
  - `NcpClient._adapter: PublicAdapter | GovAdapter | FinAdapter`
  - Public package API: `from ncp_api import NcpClient, NcpEnv, NcpError, NcpAuthError, NcpApiError, NcpNetworkError`

- [ ] **Step 1: Write failing tests**

Create `tests/test_client.py`:

```python
from __future__ import annotations

import os

import pytest

from ncp_api import NcpApiError, NcpAuthError, NcpClient, NcpEnv, NcpError, NcpNetworkError
from ncp_api.adapters.fin import FinAdapter
from ncp_api.adapters.gov import GovAdapter
from ncp_api.adapters.public import PublicAdapter
from ncp_api.environment import BASE_URLS


def test_default_env_is_public() -> None:
    client = NcpClient(access_key="k", secret_key="s")
    assert isinstance(client._adapter, PublicAdapter)


def test_env_param_string_public() -> None:
    client = NcpClient(access_key="k", secret_key="s", env="public")
    assert isinstance(client._adapter, PublicAdapter)


def test_env_param_string_gov() -> None:
    client = NcpClient(access_key="k", secret_key="s", env="gov")
    assert isinstance(client._adapter, GovAdapter)


def test_env_param_string_fin() -> None:
    client = NcpClient(access_key="k", secret_key="s", env="fin")
    assert isinstance(client._adapter, FinAdapter)


def test_env_param_enum_public() -> None:
    client = NcpClient(access_key="k", secret_key="s", env=NcpEnv.PUBLIC)
    assert isinstance(client._adapter, PublicAdapter)


def test_env_param_enum_gov() -> None:
    client = NcpClient(access_key="k", secret_key="s", env=NcpEnv.GOV)
    assert isinstance(client._adapter, GovAdapter)


def test_env_param_enum_fin() -> None:
    client = NcpClient(access_key="k", secret_key="s", env=NcpEnv.FIN)
    assert isinstance(client._adapter, FinAdapter)


def test_env_from_env_var_gov(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NCP_ENV", "gov")
    client = NcpClient(access_key="k", secret_key="s")
    assert isinstance(client._adapter, GovAdapter)


def test_env_from_env_var_fin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NCP_ENV", "fin")
    client = NcpClient(access_key="k", secret_key="s")
    assert isinstance(client._adapter, FinAdapter)


def test_env_param_overrides_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NCP_ENV", "gov")
    client = NcpClient(access_key="k", secret_key="s", env="fin")
    assert isinstance(client._adapter, FinAdapter)


def test_invalid_env_raises_value_error() -> None:
    with pytest.raises(ValueError):
        NcpClient(access_key="k", secret_key="s", env="invalid")


def test_adapter_base_url_matches_env_public() -> None:
    client = NcpClient(access_key="k", secret_key="s", env="public")
    assert client._adapter.base_url == BASE_URLS[NcpEnv.PUBLIC]


def test_adapter_base_url_matches_env_gov() -> None:
    client = NcpClient(access_key="k", secret_key="s", env="gov")
    assert client._adapter.base_url == BASE_URLS[NcpEnv.GOV]


def test_imports_from_package_root() -> None:
    assert NcpClient is not None
    assert NcpEnv is not None
    assert NcpError is not None
    assert NcpAuthError is not None
    assert NcpApiError is not None
    assert NcpNetworkError is not None
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_client.py -v
```

Expected: `ModuleNotFoundError: No module named 'ncp_api.adapters.public'`

- [ ] **Step 3: Create adapter scaffolding**

Create `src/ncp_api/adapters/public/__init__.py`:

```python
from __future__ import annotations

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.auth import HmacSigner


class PublicAdapter(NcpHttpAdapter):
    """Adapter for NCP Public cloud environment."""

    def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
        super().__init__(env_base_url, signer)
```

Create `src/ncp_api/adapters/gov/__init__.py`:

```python
from __future__ import annotations

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.auth import HmacSigner


class GovAdapter(NcpHttpAdapter):
    """Adapter for NCP Government cloud environment."""

    def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
        super().__init__(env_base_url, signer)
```

Create `src/ncp_api/adapters/fin/__init__.py`:

```python
from __future__ import annotations

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.auth import HmacSigner


class FinAdapter(NcpHttpAdapter):
    """Adapter for NCP Financial cloud environment."""

    def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
        super().__init__(env_base_url, signer)
```

- [ ] **Step 4: Implement NcpClient**

Create `src/ncp_api/client.py`:

```python
from __future__ import annotations

import os
from typing import Union

from ncp_api.adapters.fin import FinAdapter
from ncp_api.adapters.gov import GovAdapter
from ncp_api.adapters.public import PublicAdapter
from ncp_api.auth import HmacSigner
from ncp_api.environment import BASE_URLS, NcpEnv


class NcpClient:
    """Entry point for the NCP API client.

    Environment resolution order:
    1. ``env`` constructor parameter
    2. ``NCP_ENV`` environment variable
    3. Default: ``"public"``
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        env: Union[str, NcpEnv, None] = None,
    ) -> None:
        resolved = NcpEnv(env or os.environ.get("NCP_ENV", "public"))
        signer = HmacSigner(access_key, secret_key)
        base_url = BASE_URLS[resolved]

        if resolved is NcpEnv.PUBLIC:
            self._adapter: Union[PublicAdapter, GovAdapter, FinAdapter] = PublicAdapter(base_url, signer)
        elif resolved is NcpEnv.GOV:
            self._adapter = GovAdapter(base_url, signer)
        else:
            self._adapter = FinAdapter(base_url, signer)
```

- [ ] **Step 5: Update src/ncp_api/__init__.py**

Replace the entire file:

```python
from ncp_api.client import NcpClient
from ncp_api.environment import NcpEnv
from ncp_api.exceptions import NcpApiError, NcpAuthError, NcpError, NcpNetworkError

__version__ = "0.1.0"

__all__ = [
    "NcpClient",
    "NcpEnv",
    "NcpError",
    "NcpAuthError",
    "NcpApiError",
    "NcpNetworkError",
]
```

- [ ] **Step 6: Run all tests**

```bash
uv run pytest -v
```

Expected: all tests pass (Task 1 + 2 + 3 + 4 tests).

- [ ] **Step 7: Verify mypy and ruff**

```bash
uv run mypy src/
uv run ruff check .
```

Expected: both exit 0.

- [ ] **Step 8: Commit**

```bash
git add src/ncp_api/adapters/public/ src/ncp_api/adapters/gov/ src/ncp_api/adapters/fin/ src/ncp_api/client.py src/ncp_api/__init__.py tests/test_client.py
git commit -m "feat: add adapter scaffolding and NcpClient entry point"
```
