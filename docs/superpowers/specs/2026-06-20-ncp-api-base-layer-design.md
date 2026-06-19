# NCP API Base Layer Design

**Date:** 2026-06-20  
**Status:** Approved

## Overview

Base layer for `ncp-api-python` — a Python client library for Naver Cloud Platform (NCP) APIs. Supports three environments (Public, Gov, Fin) with HMAC authentication, sync/async HTTP via httpx, and a Composition-based Adapter pattern for environment and service isolation.

This spec covers the **base layer only**: auth, HTTP, environment config, error types, and adapter scaffolding. Individual service APIs (Server, VPC, Object Storage, etc.) are added per subsequent specs.

## Architecture

```
NcpClient (entry point)
  └── resolves env → instantiates adapter

PublicAdapter / GovAdapter / FinAdapter
  └── NcpHttpAdapter (base)
        ├── HmacSigner (auth)
        └── httpx.Client + httpx.AsyncClient (HTTP)

# Future service addition (composition):
PublicAdapter
  └── self.server = ServerApi(base_url, signer)
  └── self.vpc    = VpcApi(base_url, signer)
```

## File Structure

```
src/ncp_api/
├── __init__.py              # Re-exports: NcpClient, NcpError, NcpEnv
├── client.py                # NcpClient — user entry point
├── environment.py           # NcpEnv enum + BASE_URLS dict
├── auth.py                  # HmacSigner
├── exceptions.py            # NcpError hierarchy
└── adapters/
    ├── __init__.py
    ├── base.py              # NcpHttpAdapter (common HTTP + auth)
    ├── public/
    │   └── __init__.py      # PublicAdapter
    ├── gov/
    │   └── __init__.py      # GovAdapter
    └── fin/
        └── __init__.py      # FinAdapter
```

## Components

### `exceptions.py`

```python
class NcpError(Exception): ...

class NcpAuthError(NcpError):
    """401 responses or HMAC signature failures."""

class NcpApiError(NcpError):
    """Non-2xx API responses with NCP error body."""
    status_code: int
    error_code: str
    message: str

class NcpNetworkError(NcpError):
    """Connection failures, timeouts."""
```

### `environment.py`

```python
class NcpEnv(str, Enum):
    PUBLIC = "public"
    GOV = "gov"
    FIN = "fin"

BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://ncloud.apigw.ntruss.com",
    NcpEnv.GOV:    "https://ncloud.apigw.gov-ntruss.com",
    NcpEnv.FIN:    "https://ncloud.apigw.fin-ntruss.com",
}
```

### `auth.py` — HmacSigner

NCP HMAC-SHA256 signature per spec:
- String to sign: `"{METHOD}\n{URL_PATH_AND_QUERY}\n{TIMESTAMP}\n{ACCESS_KEY}"`
- Signature: `base64(HMAC-SHA256(secret_key.encode(), string_to_sign.encode()))`

```python
class HmacSigner:
    def __init__(self, access_key: str, secret_key: str) -> None: ...

    def sign(self, method: str, url: str, timestamp: int) -> dict[str, str]:
        """Returns auth headers for a single request."""
        # Returns:
        # {
        #   "x-ncp-apigw-timestamp": str(timestamp),
        #   "x-ncp-iam-access-key": self.access_key,
        #   "x-ncp-apigw-signature-v2": <base64-encoded signature>,
        # }
```

`url` passed to `sign()` is the path + query string only (not the full URL), matching NCP spec.

### `adapters/base.py` — NcpHttpAdapter

URL resolution:
- `base_url`: environment default, injected at construction
- `path_prefix`: class-level constant, defined by each service subclass (default `""`)
- `_resolve_url(path)` → `f"{self.base_url}{self.path_prefix}{path}"`
- Service with a different domain sets `base_url` as a class variable to override

```python
class NcpHttpAdapter:
    path_prefix: str = ""
    _service_base_url: ClassVar[str | None] = None  # set by services with own domain

    def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
        self._env_base_url = env_base_url   # env default (injected)
        self._signer = signer
        self._client = httpx.Client()
        self._async_client = httpx.AsyncClient()

    @property
    def base_url(self) -> str:
        return self._service_base_url or self._env_base_url

    def request(
        self, method: str, path: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Sync request. Raises NcpAuthError / NcpApiError / NcpNetworkError."""

    async def arequest(
        self, method: str, path: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Async request. Same error contract as request()."""

    def _resolve_url(self, path: str) -> str:
        return f"{self.base_url}{self.path_prefix}{path}"

    def _make_headers(self, method: str, path: str) -> dict[str, str]:
        timestamp = int(time.time() * 1000)
        return self._signer.sign(method, path, timestamp)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        # 401 → NcpAuthError
        # other 4xx/5xx → NcpApiError(status_code, error_code, message)
        # JSON parse error → NcpApiError
```

httpx exceptions mapping:
- `httpx.ConnectError`, `httpx.TimeoutException` → `NcpNetworkError`
- `httpx.HTTPStatusError` with 401 → `NcpAuthError`
- `httpx.HTTPStatusError` otherwise → `NcpApiError`

### `adapters/public/__init__.py` — PublicAdapter

```python
class PublicAdapter(NcpHttpAdapter):
    """Public cloud environment adapter.
    
    Service attributes added here as NCP services are implemented:
    self.server = ServerApi(base_url, signer)
    """
```

`GovAdapter` and `FinAdapter` follow the identical pattern.

### `client.py` — NcpClient

Environment resolution priority: constructor `env` parameter → `NCP_ENV` env var → `"public"` default.

```python
class NcpClient:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        env: str | NcpEnv | None = None,
    ) -> None:
        resolved = NcpEnv(env or os.environ.get("NCP_ENV", "public"))
        signer = HmacSigner(access_key, secret_key)
        base_url = BASE_URLS[resolved]

        if resolved == NcpEnv.PUBLIC:
            self._adapter = PublicAdapter(base_url, signer)
        elif resolved == NcpEnv.GOV:
            self._adapter = GovAdapter(base_url, signer)
        else:
            self._adapter = FinAdapter(base_url, signer)
```

Invalid `env` values raise `ValueError` from `NcpEnv(...)`.

### `__init__.py` — Public API

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

## URL Resolution — Service Override Pattern

Default (env base_url + path prefix):
```python
class ServerApi(NcpHttpAdapter):
    path_prefix = "/vserver/v2"
    # base_url inherited from adapter constructor (env default)
```

Domain override (service has its own domain):
```python
class ObjectStorageApi(NcpHttpAdapter):
    _service_base_url = "https://kr.object.ncloudstorage.com"
    path_prefix = ""
    # _service_base_url takes priority over injected env_base_url via base_url property
```

## Dependencies

Add to `pyproject.toml`:
```toml
[project]
dependencies = ["httpx>=0.27.0"]
```

## Testing Strategy

- `HmacSigner`: unit test signature output against known vector (method, url, timestamp, keys → expected header values)
- `NcpHttpAdapter.request`: use `httpx.MockTransport` — no live network calls
- `NcpClient`: test env resolution (param → env var → default), test ValueError on invalid env
- `_handle_response`: test each HTTP status → correct exception type and fields
- No mocking of `HmacSigner` in adapter tests — real signer, mocked HTTP

## Usage Examples

```python
from ncp_api import NcpClient, NcpEnv

# Public (default)
client = NcpClient(access_key="KEY", secret_key="SECRET")

# Gov via parameter
client = NcpClient(access_key="KEY", secret_key="SECRET", env="gov")

# Fin via enum
client = NcpClient(access_key="KEY", secret_key="SECRET", env=NcpEnv.FIN)

# Fin via env var (NCP_ENV=fin python script.py)
client = NcpClient(access_key="KEY", secret_key="SECRET")

# Future service usage (after ServerApi added)
instances = client.server.get_instance_list()

# Async
instances = await client.server.aget_instance_list()
```

## Constraints

- Python `>=3.9`
- `httpx>=0.27.0` only runtime dependency
- mypy strict — all public interfaces fully typed
- No service implementations in this spec — adapters are empty scaffolding
