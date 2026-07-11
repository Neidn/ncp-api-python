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

result = client.server.get_server_instance_list(server_name="my-server", page_no=0, page_size=20)
servers = result["serverInstanceList"]

# Async
result = await client.server.aget_server_instance_list(server_name="my-server")
```

## Environments

```python
client = NcpClient(access_key="KEY", secret_key="SECRET")              # Public (default)
client = NcpClient(access_key="KEY", secret_key="SECRET", env="gov")   # Gov
client = NcpClient(access_key="KEY", secret_key="SECRET", env="fin")   # Fin

# Via environment variable
# NCP_ENV=gov python script.py
```

## Error Handling

```python
from ncp_api import NcpAuthError, NcpApiError, NcpRateLimitError, NcpNetworkError

try:
    result = client.server.get_server_instance_list()
except NcpAuthError as e:
    print(e.error_code, e)       # 200: invalid credentials, 210: permission denied
except NcpRateLimitError as e:
    print(e.error_code, e)       # 400: quota exceeded, 410: throttle, 420: rate limited
except NcpApiError as e:
    print(e.status_code, e.error_code, e.message)
except NcpNetworkError:
    ...
```

`NcpRateLimitError` is a subclass of `NcpApiError`. Catch it first to handle separately (e.g., retry with backoff).

## Client Lifecycle

```python
with NcpClient(access_key="KEY", secret_key="SECRET") as client:
    result = client.server.get_server_instance_list()

async with NcpClient(access_key="KEY", secret_key="SECRET") as client:
    result = await client.server.aget_server_instance_list()
```

## Supported APIs

All methods have an async counterpart prefixed with `a` (e.g. `aget_server_instance_list`).

### Compute

| Service | `client.*` | Key Methods |
|---------|-----------|-------------|
| Server | `server` | `get_server_instance_list`, `create_server_instances`, `stop/start/reboot/terminate_server_instances`, `get_public_ip_instance_list` |
| Block Storage | `block_storage` | `get_block_storage_instance_list`, `create/delete_block_storage_instance` |
| NAS | `nas` | `get_nas_volume_instance_list`, `create/delete_nas_volume_instance` |

### Networking

| Service | `client.*` | Key Methods |
|---------|-----------|-------------|
| VPC | `vpc` | `get_vpc_list`, `create/delete_vpc`, `get_subnet_list`, `get_nat_gateway_instance_list`, `get_vpc_peering_instance_list`, `get_route_table_list` |
| Load Balancer | `load_balancer` | `get_load_balancer_instance_list`, `create/delete_load_balancer_instance` |
| Global DNS | `global_dns` | `get_domain_list`, `get_record_list`, `create/delete_record` |
| CDN | `cdn` | `get_cdn_plus_instance_list`, `request_cdn_plus_purge`, `get_global_cdn_instance_list` |

### Storage

| Service | `client.*` | Key Methods |
|---------|-----------|-------------|
| Object Storage | `object_storage` | `list_buckets`, `list_objects`, `put_object`, `get_object`, `delete_object` |

### Database

| Service | `client.*` | Key Methods |
|---------|-----------|-------------|
| Cloud DB for MySQL | `mysql` | `get_cloud_mysql_instance_list`, `create/delete_cloud_mysql_instance` |
| Cloud DB for MongoDB | `mongodb` | `get_cloud_mongodb_instance_list`, `create/delete_cloud_mongodb_instance` |
| Cloud DB for PostgreSQL | `postgresql` | `get_cloud_postgresql_instance_list`, `create/delete_cloud_postgresql_instance` |
| Cloud DB for Cache | `cache` | `get_cloud_cache_instance_list`, `create/delete_cloud_cache_instance` |
| Cloud DB for Redis | `redis` | `get_cloud_redis_instance_list`, `create/delete_cloud_redis_instance` |
| Cloud MSSQL | `mssql` | `get_cloud_mssql_instance_list`, `create/delete_cloud_mssql_instance`, `get_cloud_mssql_image_product_list` |
| Classic Cloud DB | `cloud_db` | `get_cloud_db_instance_list`, `create/delete_cloud_db_instance`, `reboot/flush_cloud_db_instance` |

### Platform

| Service | `client.*` | Key Methods |
|---------|-----------|-------------|
| NKS (Kubernetes) | `nks` | `get_cluster_list`, `create/delete_cluster`, `get_worker_nodes`, `get_node_pool` |
| Cloud Hadoop | `hadoop` | `get_cloud_hadoop_instance_list`, `create/delete_cloud_hadoop_instance`, `change_node_count/spec` |
| Cloud Data Streaming (CDSS) | `cdss` | `get_cluster_list`, `create/delete_cluster`, `get_config_group_list`, `create/delete_config_group`, `get_kafka_version_list` |
| Cloud Search Engine (SES) | `search_engine` | `get_cluster_list`, `create/delete_cluster`, `get_snapshot_list`, `create/restore_snapshot`, `start_import` |

### Auto Scaling

| Service | `client.*` | Key Methods |
|---------|-----------|-------------|
| VPC Auto Scaling | `auto_scaling` | `get_auto_scaling_group_list`, `create/delete_auto_scaling_group`, `get_launch_configuration_list`, `create/delete_launch_configuration`, `put/delete_scaling_policy`, `get_scheduled_action_list` |
| Classic Auto Scaling | `classic_auto_scaling` | `get_auto_scaling_group_list`, `create/delete_auto_scaling_group`, `get_launch_configuration_list`, `get_adjustment_type_list` |

### Management

| Service | `client.*` | Key Methods |
|---------|-----------|-------------|
| Cloud Insight | `cloud_insight` | `query_data_multiple`, `get_system_schema_key_list`, `get_servers_top` |

### DevOps (Source Tools)

| Service | `client.*` | Key Methods |
|---------|-----------|-------------|
| Source Commit | `source_commit` | `get_repositories`, `get_repository`, `create/delete/change_repository` |
| Source Build | `source_build` | `get_projects`, `create/change/delete_project`, `start/cancel_build`, `get_build_history` |
| Source Pipeline | `source_pipeline` | `get_projects`, `create/change/delete_project`, `start_project`, `get_project_histories` |
| VPC Source Pipeline | `vpc_source_pipeline` | same methods as `source_pipeline` (VPC environment) |
| VPC Source Deploy | `vpc_source_deploy` | `get_projects`, `create/delete_project`, `get/create/change/delete_stage`, `get/create/change/delete_scenario`, `deploy`, `accept/reject_deploy_approval`, `accept/reject_deploy_canary` |

## Development

```bash
make dev        # install all deps
make check      # lint + typecheck + test
make test       # pytest only
make lint       # ruff check
make typecheck  # mypy
```

Requires [uv](https://docs.astral.sh/uv/).

### Integration Tests

Unit tests use mocked HTTP. To run against the live NCP API, create a `.env` file in the project root:

```ini
NCP_ACCESS_KEY=ncp_iam_...
NCP_SECRET_KEY=ncp_iam_...
NCP_ENV=public
```

```bash
uv run pytest tests/test_integration.py -v
```

Integration tests are automatically skipped when credentials are not present. All integration tests are read-only (list/get only — no resources are created or modified).
