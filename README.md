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

## Cloud Insight

Query metric data from [NCP Cloud Insight](https://www.ncloud.com/product/management/cloudInsight).

### query_data_multiple

```python
from ncp_api import NcpClient
from ncp_api.adapters.cloud_insight import MetricInfo

client = NcpClient(access_key="KEY", secret_key="SECRET")

import time

now_ms = int(time.time() * 1000)

results = client.cloud_insight.query_data_multiple(
    time_start=now_ms - 30 * 60 * 1000,   # Unix timestamp in milliseconds
    time_end=now_ms,
    metric_info_list=[
        MetricInfo(
            prod_key="460438474722512896",        # Server(VPC) — see get_system_schema_key_list
            metric="avg_cpu_used_rto",
            interval="Min5",                      # Min1, Min5, Min30, Hour2, Day1
            dimensions={"instanceNo": "12345"},
            aggregation="AVG",                    # COUNT, SUM, MAX, MIN, AVG (default: AVG)
        ),
        MetricInfo(
            prod_key="460438474722512896",
            metric="mem_usert",
            interval="Min5",
            dimensions={"instanceNo": "12345"},
            aggregation="MAX",
            query_aggregation="SUM",              # optional: aggregation across query window
        ),
    ],
)

# results is a list — one entry per MetricInfo
for r in results:
    print(r["metric"])   # "avg_cpu_used_rto"
    print(r["dps"])      # [[timestamp_ms, value], ...]
```

Async:

```python
results = await client.cloud_insight.aquery_data_multiple(
    time_start=now_ms - 30 * 60 * 1000,
    time_end=now_ms,
    metric_info_list=[MetricInfo(...)],
)
```

Up to 20 metrics per call.

#### Server(VPC) confirmed metric names

| metric | description |
|--------|-------------|
| `avg_cpu_used_rto` | CPU usage (%) |
| `mem_usert` | Memory usage (%) |
| `avg_fs_usert` | Filesystem usage (%) |
| `avg_snd_bps` | Network outbound (bps) |
| `avg_rcv_bps` | Network inbound (bps) |

Get `prod_key` values for all services via `get_system_schema_key_list`.

### get_system_schema_key_list

Returns all NCP services available in Cloud Insight with their `cw_key` (used as `prod_key` in `query_data_multiple`).

```python
schemas = client.cloud_insight.get_system_schema_key_list()
# [{"cw_key": "460438474722512896", "prodName": "Server(VPC)"}, ...]

for s in schemas:
    print(s["cw_key"], s["prodName"])

# Async
schemas = await client.cloud_insight.aget_system_schema_key_list()
```

### get_servers_top

Returns the top 5 servers by CPU, memory, or filesystem usage.

```python
# query: "avg_cpu_used_rto" | "mem_usert" | "avg_fs_usert"
# prod:  "VPC" (default) | "Classic"
results = client.cloud_insight.get_servers_top(query="avg_cpu_used_rto")
results = client.cloud_insight.get_servers_top(query="mem_usert", prod="Classic")

for server in results:
    print(server["hostName"], server["avg_cpu_used_rto"])

# Async
results = await client.cloud_insight.aget_servers_top(query="avg_fs_usert")
```

## Cloud DB for MySQL

```python
result = client.mysql.get_cloud_mysql_instance_list()
instances = result["cloudMysqlInstanceList"]
total = result["totalRows"]

# With filters
result = client.mysql.get_cloud_mysql_instance_list(
    vpc_no="123",
    cloud_mysql_service_name="my-db",
    generation_code="G2",           # "G2" | "G3"
    page_no=0,
    page_size=20,
)

# Filter by instance numbers
result = client.mysql.get_cloud_mysql_instance_list(
    cloud_mysql_instance_no_list=["111111", "222222"],
)

# Async
result = await client.mysql.aget_cloud_mysql_instance_list(vpc_no="123")
```

## Cloud DB for MongoDB

```python
result = client.mongodb.get_cloud_mongodb_instance_list()
instances = result["cloudMongoDbInstanceList"]
total = result["totalRows"]

# With filters
result = client.mongodb.get_cloud_mongodb_instance_list(
    vpc_no="456",
    cloud_mongodb_service_name="my-mongo",
    generation_code="G3",           # "G2" | "G3"
    page_no=0,
    page_size=20,
)

# Filter by instance numbers
result = client.mongodb.get_cloud_mongodb_instance_list(
    cloud_mongodb_instance_no_list=["333333", "444444"],
)

# Async
result = await client.mongodb.aget_cloud_mongodb_instance_list(vpc_no="456")
```

## Cloud DB for PostgreSQL

```python
result = client.postgresql.get_cloud_postgresql_instance_list()
instances = result["cloudPostgresqlInstanceList"]
total = result["totalRows"]

# With filters
result = client.postgresql.get_cloud_postgresql_instance_list(
    vpc_no="123",
    cloud_postgresql_service_name="my-postgres",
    page_no=0,
    page_size=20,
)

# Filter by instance numbers
result = client.postgresql.get_cloud_postgresql_instance_list(
    cloud_postgresql_instance_no_list=["111111", "222222"],
)

# Async
result = await client.postgresql.aget_cloud_postgresql_instance_list(vpc_no="123")
```

## NKS (Naver Kubernetes Service)

```python
# Cluster list
clusters = client.nks.get_cluster_list()                      # KR (default)
clusters = client.nks.get_cluster_list(region_code="SGN")     # Singapore
clusters = client.nks.get_cluster_list(region_code="JPN")     # Japan

for c in clusters:
    print(c["name"], c["status"], c["k8sVersion"])

# Worker nodes
nodes = client.nks.get_worker_nodes("cluster-uuid")
nodes = client.nks.get_worker_nodes("cluster-uuid", region_code="SGN")

for n in nodes:
    print(n["name"], n["k8sStatus"], n["privateIp"])

# Node pools
pools = client.nks.get_node_pool("cluster-uuid")
pools = client.nks.get_node_pool("cluster-uuid", hypervisor_code="KVM")  # XEN (default) | KVM

for p in pools:
    print(p["name"], p["nodeCount"], p["status"])

# Async
clusters = await client.nks.aget_cluster_list()
nodes    = await client.nks.aget_worker_nodes("cluster-uuid")
pools    = await client.nks.aget_node_pool("cluster-uuid")
```

Regions: `"KR"` (default), `"SGN"`, `"JPN"`. Gov environment additionally supports `"KRS"` (Busan).

## Object Storage

S3-compatible object storage. Uses AWS Signature V4 auth (not NCP HMAC) and returns structured dicts parsed from XML.

```python
# List buckets
result = client.object_storage.list_buckets()
buckets = result["buckets"]   # [{"name": ..., "creationDate": ...}]
owner = result["owner"]       # {"id": ..., "displayName": ...}

# List objects in a bucket
result = client.object_storage.list_objects("my-bucket")
for obj in result["contents"]:
    print(obj["key"], obj["size"], obj["lastModified"])

# With filters
result = client.object_storage.list_objects(
    "my-bucket",
    prefix="logs/2024/",      # filter by prefix
    delimiter="/",             # group by delimiter → result["commonPrefixes"]
    max_keys=100,              # default 1000
    marker="logs/2024/01/",   # pagination cursor
)
print(result["isTruncated"])       # True if more results exist
print(result["commonPrefixes"])    # ["logs/2024/01/", "logs/2024/02/"]

# Async
result = await client.object_storage.alist_buckets()
result = await client.object_storage.alist_objects("my-bucket", prefix="logs/")
```

Endpoints by environment:

| Environment | Base URL |
|-------------|----------|
| Public | `https://kr.object.ncloudstorage.com` |
| Gov | `https://kr.object.gov-ncloudstorage.com` |
| Fin | `https://kr.object.fin-ncloudstorage.com` |

## Block Storage

```python
result = client.block_storage.get_block_storage_instance_list()
volumes = result["blockStorageInstanceList"]
total = result["totalRows"]

# With filters
result = client.block_storage.get_block_storage_instance_list(
    server_instance_no="140599555",           # attached server
    block_storage_status_code="ATTAC",        # INIT | CREAT | ATTAC | DETAC | TERMTING
    block_storage_type_code="BASIC",          # BASIC | SSDP1 | SSDP2
    block_storage_disk_type_code="NET",
    block_storage_disk_detail_type_code="SSD",
    page_no=0,
    page_size=20,
    sorted_by="blockStorageName",
    sorting_order="ASC",
)

# Filter by instance numbers
result = client.block_storage.get_block_storage_instance_list(
    block_storage_instance_no_list=["555555", "666666"],
)

# Async
result = await client.block_storage.aget_block_storage_instance_list(server_instance_no="140599555")
```

## VPC

```python
# VPC list
result = client.vpc.get_vpc_list()
vpcs = result["vpcList"]
total = result["totalRows"]

# With filters
result = client.vpc.get_vpc_list(
    vpc_name="my-vpc",
    vpc_status_code="RUN",    # INIT | CREATING | RUN | TERMTING
)

# Filter by VPC numbers
result = client.vpc.get_vpc_list(vpc_no_list=["12345", "67890"])

# Async
result = await client.vpc.aget_vpc_list()
```

```python
# Subnet list
result = client.vpc.get_subnet_list()
subnets = result["subnetList"]
total = result["totalRows"]

# With filters
result = client.vpc.get_subnet_list(
    vpc_no="12345",
    zone_code="KR-1",
    subnet_type_code="PUBLIC",      # PUBLIC | PRIVATE
    usage_type_code="GEN",          # GEN | LOADB | BM | NATGW
    subnet_status_code="RUN",       # INIT | CREATING | RUN | TERMTING
    subnet_name="my-subnet",
    subnet="10.0.1.0/24",
    network_acl_no="777",
    page_no=0,
    page_size=20,
)

# Filter by subnet numbers
result = client.vpc.get_subnet_list(subnet_no_list=["99999", "88888"])

# Async
result = await client.vpc.aget_subnet_list(vpc_no="12345")
```

## Cloud DB for Cache (Redis / Valkey)

NCP provides two Cache APIs: a newer unified API (`/vcache/v2`) supporting both Redis and Valkey, and a legacy Redis-only API (`/vredis/v2`).

```python
# Newer API — Redis and Valkey
result = client.cache.get_cloud_cache_instance_list()
instances = result["cloudCacheInstanceList"]
total = result["totalRows"]

# Filter by DBMS type
result = client.cache.get_cloud_cache_instance_list(
    cloud_cache_dbms_code="Redis",    # "Redis" | "Valkey"
    vpc_no="123",
    cloud_cache_service_name="my-cache",
    generation_code="G3",             # "G2" | "G3"
    page_no=0,
    page_size=20,
)

# Filter by instance numbers
result = client.cache.get_cloud_cache_instance_list(
    cloud_cache_instance_no_list=["111111", "222222"],
)

# Async
result = await client.cache.aget_cloud_cache_instance_list(cloud_cache_dbms_code="Redis")
```

```python
# Legacy Redis-only API
result = client.redis.get_cloud_redis_instance_list()
instances = result["cloudRedisInstanceList"]
total = result["totalRows"]

# With filters
result = client.redis.get_cloud_redis_instance_list(
    vpc_no="456",
    cloud_redis_service_name="my-redis",
    generation_code="G2",
    page_no=0,
    page_size=20,
)

# Async
result = await client.redis.aget_cloud_redis_instance_list(vpc_no="456")
```

## NAS

```python
result = client.nas.get_nas_volume_instance_list()
volumes = result["nasVolumeInstanceList"]
total = result["totalRows"]

# With filters
result = client.nas.get_nas_volume_instance_list(
    zone_code="KR-1",
    volume_name="my-nas",
    volume_allotment_protocol_type_code="NFS",   # "NFS" | "CIFS"
    is_snapshot_configuration=True,
    is_event_configuration=False,
    page_no=0,
    page_size=20,
    sorted_by="volumeName",                       # nasVolumeInstanceNo | volumeName | volumeTotalSize
    sorting_order="ASC",                          # ASC (default) | DESC
)

# Filter by instance numbers
result = client.nas.get_nas_volume_instance_list(
    nas_volume_instance_no_list=["111111", "222222"],
)

# Async
result = await client.nas.aget_nas_volume_instance_list(zone_code="KR-1")
```

## Supported APIs

| Service | `client.*` | Method | Description |
|---------|-----------|--------|-------------|
| Server | `server` | `get_server_instance_list` | List VPC server instances |
| Object Storage | `object_storage` | `list_buckets` | List S3-compatible buckets |
| Object Storage | `object_storage` | `list_objects` | List objects in a bucket |
| Block Storage | `block_storage` | `get_block_storage_instance_list` | List block storage volumes |
| NAS | `nas` | `get_nas_volume_instance_list` | List NAS volume instances |
| VPC | `vpc` | `get_vpc_list` | List VPCs |
| VPC | `vpc` | `get_subnet_list` | List subnets |
| Cloud DB for MySQL | `mysql` | `get_cloud_mysql_instance_list` | List MySQL instances |
| Cloud DB for MongoDB | `mongodb` | `get_cloud_mongodb_instance_list` | List MongoDB instances |
| Cloud DB for PostgreSQL | `postgresql` | `get_cloud_postgresql_instance_list` | List PostgreSQL instances |
| Cloud DB for Cache | `cache` | `get_cloud_cache_instance_list` | List Cache instances (Redis / Valkey) |
| Cloud DB for Redis | `redis` | `get_cloud_redis_instance_list` | List Redis instances (legacy) |
| NKS | `nks` | `get_cluster_list` | List Kubernetes clusters by region |
| NKS | `nks` | `get_worker_nodes` | List worker nodes in a cluster |
| NKS | `nks` | `get_node_pool` | List node pools in a cluster |
| Cloud Insight | `cloud_insight` | `get_system_schema_key_list` | List all services with their `cw_key` |
| Cloud Insight | `cloud_insight` | `query_data_multiple` | Query metric time-series data (up to 20 metrics) |
| Cloud Insight | `cloud_insight` | `get_servers_top` | Top 5 servers by CPU / memory / filesystem usage |

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

Unit tests use mocked HTTP. To run tests against the live NCP API, create a `.env` file in the project root:

```bash
cp .env.example .env
# fill in your credentials
```

```ini
NCP_ACCESS_KEY=ncp_iam_...
NCP_SECRET_KEY=ncp_iam_...
NCP_ENV=public
```

Then run:

```bash
# integration tests only
uv run pytest tests/test_integration.py -v

# all tests (unit + integration)
uv run pytest -v
```

Integration tests are automatically skipped when credentials are not present.
