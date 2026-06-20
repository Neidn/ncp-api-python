# ncp-api-python

Python client library for [Naver Cloud Platform (NCP)](https://www.ncloud.com) APIs.

## Installation

```bash
uv add git+https://github.com/Neidn/ncp-api-python@v0.1.0
```

## Quick Start

```python
from ncp_api import NcpClient

client = NcpClient(access_key="YOUR_ACCESS_KEY", secret_key="YOUR_SECRET_KEY")

# List all server instances
result = client.server.get_server_instance_list()
servers = result["serverInstanceList"]

# With filters
result = client.server.get_server_instance_list(
    server_name="my-server",
    server_instance_status_code="RUN",
    page_no=0,
    page_size=20,
)

# Async
result = await client.server.aget_server_instance_list(server_name="my-server")
```

## Environments

NCP supports three environments. Select via constructor, environment variable, or default.

```python
# Public (default)
client = NcpClient(access_key="KEY", secret_key="SECRET")

# Gov
client = NcpClient(access_key="KEY", secret_key="SECRET", env="gov")

# Fin
from ncp_api import NcpEnv
client = NcpClient(access_key="KEY", secret_key="SECRET", env=NcpEnv.FIN)

# Via environment variable
# NCP_ENV=gov python script.py
client = NcpClient(access_key="KEY", secret_key="SECRET")
```

## Error Handling

```python
from ncp_api import (
    NcpAuthError,
    NcpApiError,
    NcpRateLimitError,
    NcpNetworkError,
)

try:
    result = client.server.get_server_instance_list()
except NcpAuthError as e:
    # HTTP 401
    # e.error_code == "200" → invalid credentials (check access/secret key)
    # e.error_code == "210" → permission denied (check sub-account permissions)
    print(e.error_code, e)
except NcpRateLimitError as e:
    # HTTP 429 — quota or rate limit hit
    # e.error_code == "400" → quota exceeded
    # e.error_code == "410" → throttle limited
    # e.error_code == "420" → rate limited
    print(e.error_code, e.message)
except NcpApiError as e:
    # Other non-2xx responses
    print(e.status_code, e.error_code, e.message)
except NcpNetworkError:
    # Connection failure or timeout
    ...
```

`NcpRateLimitError` is a subclass of `NcpApiError`, so `except NcpApiError` catches it too. Catch `NcpRateLimitError` first if you want to handle rate limits separately (e.g., retry with backoff).

### Retry on Rate Limit

The library raises `NcpRateLimitError` and leaves retry strategy to the caller. Example with `tenacity`:

```python
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from ncp_api import NcpRateLimitError

@retry(
    retry=retry_if_exception_type(NcpRateLimitError),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(5),
)
def list_servers():
    return client.server.get_server_instance_list()
```

Or without a library:

```python
import time

def list_servers_with_retry(max_attempts: int = 5) -> dict:
    for attempt in range(max_attempts):
        try:
            return client.server.get_server_instance_list()
        except NcpRateLimitError:
            if attempt == max_attempts - 1:
                raise
            time.sleep(2 ** attempt)  # exponential backoff: 1s, 2s, 4s, 8s...
```

## Client Lifecycle

```python
# Sync context manager
with NcpClient(access_key="KEY", secret_key="SECRET") as client:
    result = client.server.get_server_instance_list()

# Async context manager
async with NcpClient(access_key="KEY", secret_key="SECRET") as client:
    result = await client.server.aget_server_instance_list()
```

## Supported APIs

| Service | Method | Description |
|---------|--------|-------------|
| Server | `get_server_instance_list` | List VPC server instances |

## Development

```bash
make dev        # install all deps
make check      # lint + typecheck + test
make test       # pytest only
make lint       # ruff check
make typecheck  # mypy
```

Requires [uv](https://docs.astral.sh/uv/).
