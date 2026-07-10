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

## Usage Examples

Each section shows one representative call. All methods accept keyword-only arguments — refer to the [NCP API docs](https://api.ncloud-docs.com/docs) for the full parameter list.

### Server

```python
result = client.server.get_server_instance_list(vpc_no="12345", server_instance_status_code="RUN")
servers = result["serverInstanceList"]
```

→ [getServerInstanceList](https://api.ncloud-docs.com/docs/compute-vserver-server-getserverinstancelist)

### Public IP

```python
result = client.server.get_public_ip_instance_list(is_associated=True)
ips = result["publicIpInstanceList"]
```

→ [getPublicIpInstanceList](https://api.ncloud-docs.com/docs/compute-vserver-publicip-getpublicipinstancelist)

### Block Storage

```python
result = client.block_storage.get_block_storage_instance_list(server_instance_no="140599555")
volumes = result["blockStorageInstanceList"]
```

→ [getBlockStorageInstanceList](https://api.ncloud-docs.com/docs/compute-vserver-blockstorage-getblockstorageinstancelist)

### NAS

```python
result = client.nas.get_nas_volume_instance_list(volume_allotment_protocol_type_code="NFS")
volumes = result["nasVolumeInstanceList"]
```

→ [getNasVolumeInstanceList](https://api.ncloud-docs.com/docs/storage-nas-getnasvolumeinstancelist)

### VPC

```python
result = client.vpc.get_vpc_list(vpc_status_code="RUN")
vpcs = result["vpcList"]

result = client.vpc.get_subnet_list(vpc_no="12345", subnet_type_code="PUBLIC")
subnets = result["subnetList"]
```

→ [getVpcList](https://api.ncloud-docs.com/docs/networking-vpc-vpc-getvpclist) · [getSubnetList](https://api.ncloud-docs.com/docs/networking-vpc-subnet-getsubnetlist)

### NAT Gateway

```python
result = client.vpc.get_nat_gateway_instance_list(vpc_no="12345")
gateways = result["natGatewayInstanceList"]
```

→ [getNatGatewayInstanceList](https://api.ncloud-docs.com/docs/networking-vpc-natgateway-getnatgatewayinstancelist)

### VPC Peering

```python
result = client.vpc.get_vpc_peering_instance_list(source_vpc_no="12345")
peerings = result["vpcPeeringInstanceList"]
```

→ [getVpcPeeringInstanceList](https://api.ncloud-docs.com/docs/networking-vpc-vpcpeering-getvpcpeeringinstancelist)

### Load Balancer

```python
result = client.load_balancer.get_load_balancer_instance_list(load_balancer_type_code="NETWORK")
lbs = result["loadBalancerInstanceList"]
```

→ [getLoadBalancerInstanceList](https://api.ncloud-docs.com/docs/networking-vloadbalancer-loadbalancer-getloadbalancerinstancelist)

### Cloud DB for MySQL

```python
result = client.mysql.get_cloud_mysql_instance_list(vpc_no="123")
instances = result["cloudMysqlInstanceList"]
```

→ [getCloudMysqlInstanceList](https://api.ncloud-docs.com/docs/database-clouddbformysql-getcloudmysqlinstancelist)

### Cloud DB for MongoDB

```python
result = client.mongodb.get_cloud_mongodb_instance_list(vpc_no="456")
instances = result["cloudMongoDbInstanceList"]
```

→ [getCloudMongoDbInstanceList](https://api.ncloud-docs.com/docs/database-clouddbformongodb-getcloudmongodbinstancelist)

### Cloud DB for PostgreSQL

```python
result = client.postgresql.get_cloud_postgresql_instance_list(vpc_no="123")
instances = result["cloudPostgresqlInstanceList"]
```

→ [getCloudPostgresqlInstanceList](https://api.ncloud-docs.com/docs/database-clouddbforpostgresql-getcloudpostgresqlinstancelist)

### Cloud DB for Cache (Redis / Valkey)

```python
result = client.cache.get_cloud_cache_instance_list(cloud_cache_dbms_code="Redis")
instances = result["cloudCacheInstanceList"]

# Legacy Redis-only API
result = client.redis.get_cloud_redis_instance_list(vpc_no="456")
instances = result["cloudRedisInstanceList"]
```

→ [getCloudCacheInstanceList](https://api.ncloud-docs.com/docs/database-clouddbforcache-getcloudcacheinstancelist) · [getCloudRedisInstanceList](https://api.ncloud-docs.com/docs/database-clouddbforredis-getcloudredisinstancelist)

### NKS (Naver Kubernetes Service)

```python
clusters = client.nks.get_cluster_list(region_code="KR")
nodes = client.nks.get_worker_nodes("cluster-uuid")
pools = client.nks.get_node_pool("cluster-uuid")
```

Supported regions: `KR` (default), `SGN`, `JPN`. Gov additionally supports `KRS`.

→ [NKS API docs](https://api.ncloud-docs.com/docs/platform-nks)

### Object Storage

S3-compatible; uses AWS Signature V4 auth, returns parsed XML as dicts.

```python
result = client.object_storage.list_buckets()
buckets = result["buckets"]   # [{"name": ..., "creationDate": ...}]

result = client.object_storage.list_objects("my-bucket", prefix="logs/2024/", delimiter="/", max_keys=100)
for obj in result["contents"]:
    print(obj["key"], obj["size"])
print(result["isTruncated"], result["commonPrefixes"])
```

| Environment | Base URL |
|-------------|----------|
| Public | `https://kr.object.ncloudstorage.com` |
| Gov | `https://kr.object.gov-ncloudstorage.com` |
| Fin | `https://kr.object.fin-ncloudstorage.com` |

→ [Object Storage API docs](https://api.ncloud-docs.com/docs/storage-objectstorage)

### Cloud Insight

```python
from ncp_api.adapters.cloud_insight import MetricInfo
import time

now_ms = int(time.time() * 1000)
results = client.cloud_insight.query_data_multiple(
    time_start=now_ms - 30 * 60 * 1000,
    time_end=now_ms,
    metric_info_list=[
        MetricInfo(prod_key="460438474722512896", metric="avg_cpu_used_rto", interval="Min5", dimensions={"instanceNo": "12345"}),
    ],
)
# results[0]["dps"] → [[timestamp_ms, value], ...]

schemas = client.cloud_insight.get_system_schema_key_list()
# [{"cw_key": "460438474722512896", "prodName": "Server(VPC)"}, ...]

top = client.cloud_insight.get_servers_top(query="avg_cpu_used_rto")
```

Up to 20 metrics per `query_data_multiple` call. `prod_key` values come from `get_system_schema_key_list`.

→ [Cloud Insight API docs](https://api.ncloud-docs.com/docs/management-cloudinsight)

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
| Load Balancer | `load_balancer` | `get_load_balancer_instance_list` | [→](https://api.ncloud-docs.com/docs/networking-vloadbalancer-loadbalancer-getloadbalancerinstancelist) |
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
