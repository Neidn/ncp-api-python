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
from ncp_api import NcpAuthError, NcpApiError, NcpNetworkError

try:
    result = client.server.get_server_instance_list()
except NcpAuthError:
    # 401 — invalid credentials or signature
    ...
except NcpApiError as e:
    # Non-2xx response from NCP
    print(e.status_code, e.error_code, e.message)
except NcpNetworkError:
    # Connection failure or timeout
    ...
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
