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

| Service | `client.*` | Method | NCP Doc |
|---------|-----------|--------|---------|
| Server | `server` | `get_server_instance_list` | [→](https://api.ncloud-docs.com/docs/compute-vserver-server-getserverinstancelist) |
| Server | `server` | `get_public_ip_instance_list` | [→](https://api.ncloud-docs.com/docs/compute-vserver-publicip-getpublicipinstancelist) |
| Block Storage | `block_storage` | `get_block_storage_instance_list` | [→](https://api.ncloud-docs.com/docs/compute-vserver-blockstorage-getblockstorageinstancelist) |
| NAS | `nas` | `get_nas_volume_instance_list` | [→](https://api.ncloud-docs.com/docs/storage-nas-getnasvolumeinstancelist) |
| Object Storage | `object_storage` | `list_buckets` | [→](https://api.ncloud-docs.com/docs/storage-objectstorage) |
| Object Storage | `object_storage` | `list_objects` | [→](https://api.ncloud-docs.com/docs/storage-objectstorage) |
| VPC | `vpc` | `get_vpc_list` | [→](https://api.ncloud-docs.com/docs/networking-vpc-vpc-getvpclist) |
| VPC | `vpc` | `get_subnet_list` | [→](https://api.ncloud-docs.com/docs/networking-vpc-subnet-getsubnetlist) |
| VPC | `vpc` | `get_nat_gateway_instance_list` | [→](https://api.ncloud-docs.com/docs/networking-vpc-natgateway-getnatgatewayinstancelist) |
| VPC | `vpc` | `get_vpc_peering_instance_list` | [→](https://api.ncloud-docs.com/docs/networking-vpc-vpcpeering-getvpcpeeringinstancelist) |
| VPC | `vpc` | `get_route_table_list` | [→](https://api.ncloud-docs.com/docs/networking-vpc-routetable-getroutetablelist) |
| VPC | `vpc` | `get_route_table_subnet_list` | [→](https://api.ncloud-docs.com/docs/networking-vpc-routetable-getroutetablesubnetlist) |
| VPC | `vpc` | `get_route_list` | [→](https://api.ncloud-docs.com/docs/networking-vpc-routetable-getroutelist) |
| Load Balancer | `load_balancer` | `get_load_balancer_instance_list` | [→](https://api.ncloud-docs.com/docs/networking-vloadbalancer-loadbalancer-getloadbalancerinstancelist) |
| Global DNS | `global_dns` | `get_domain_list` | [→](https://api.ncloud-docs.com/docs/networking-globaldns-record-getdomainlist) |
| Global DNS | `global_dns` | `get_record_list` | [→](https://api.ncloud-docs.com/docs/networking-globaldns-record-getrecordlist) |
| Cloud DB for MySQL | `mysql` | `get_cloud_mysql_instance_list` | [→](https://api.ncloud-docs.com/docs/database-clouddbformysql-getcloudmysqlinstancelist) |
| Cloud DB for MongoDB | `mongodb` | `get_cloud_mongodb_instance_list` | [→](https://api.ncloud-docs.com/docs/database-clouddbformongodb-getcloudmongodbinstancelist) |
| Cloud DB for PostgreSQL | `postgresql` | `get_cloud_postgresql_instance_list` | [→](https://api.ncloud-docs.com/docs/database-clouddbforpostgresql-getcloudpostgresqlinstancelist) |
| Cloud DB for Cache | `cache` | `get_cloud_cache_instance_list` | [→](https://api.ncloud-docs.com/docs/database-clouddbforcache-getcloudcacheinstancelist) |
| Cloud DB for Redis | `redis` | `get_cloud_redis_instance_list` | [→](https://api.ncloud-docs.com/docs/database-clouddbforredis-getcloudredisinstancelist) |
| NKS | `nks` | `get_cluster_list` | [→](https://api.ncloud-docs.com/docs/platform-nks) |
| NKS | `nks` | `get_worker_nodes` | [→](https://api.ncloud-docs.com/docs/platform-nks) |
| NKS | `nks` | `get_node_pool` | [→](https://api.ncloud-docs.com/docs/platform-nks) |
| Cloud Insight | `cloud_insight` | `query_data_multiple` | [→](https://api.ncloud-docs.com/docs/management-cloudinsight) |
| Cloud Insight | `cloud_insight` | `get_system_schema_key_list` | [→](https://api.ncloud-docs.com/docs/management-cloudinsight) |
| Cloud Insight | `cloud_insight` | `get_servers_top` | [→](https://api.ncloud-docs.com/docs/management-cloudinsight) |

All methods have an async counterpart prefixed with `a` (e.g. `aget_server_instance_list`), except Object Storage which uses `alist_buckets` / `alist_objects`.

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

Integration tests are automatically skipped when credentials are not present.
