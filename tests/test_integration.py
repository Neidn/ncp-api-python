"""
Live integration tests — only run when .env provides credentials.

.env (project root):
    NCP_ACCESS_KEY=ncp_iam_...
    NCP_SECRET_KEY=ncp_iam_...
    NCP_ENV=public          # optional, defaults to public

Run all:        uv run pytest tests/test_integration.py -v
Run one:        uv run pytest tests/test_integration.py::test_live_server_list -v
"""

from __future__ import annotations

import pytest

from ncp_api.client import NcpClient


def test_live_server_list(live_client: NcpClient) -> None:
    result = live_client.server.get_server_instance_list()
    assert "totalRows" in result
    assert isinstance(result["totalRows"], int)


def test_live_public_ip_list(live_client: NcpClient) -> None:
    result = live_client.server.get_public_ip_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("publicIpInstanceList", []), list)


def test_live_mysql_list(live_client: NcpClient) -> None:
    result = live_client.mysql.get_cloud_mysql_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("cloudMysqlInstanceList", []), list)


def test_live_mongodb_list(live_client: NcpClient) -> None:
    result = live_client.mongodb.get_cloud_mongodb_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("cloudMongoDbInstanceList", []), list)


def test_live_nks_cluster_list(live_client: NcpClient) -> None:
    result = live_client.nks.get_cluster_list()
    assert isinstance(result, list)


def test_live_postgresql_list(live_client: NcpClient) -> None:
    result = live_client.postgresql.get_cloud_postgresql_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("cloudPostgresqlInstanceList", []), list)


def test_live_block_storage_list(live_client: NcpClient) -> None:
    result = live_client.block_storage.get_block_storage_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("blockStorageInstanceList", []), list)


def test_live_vpc_list(live_client: NcpClient) -> None:
    result = live_client.vpc.get_vpc_list()
    assert "totalRows" in result
    assert isinstance(result.get("vpcList", []), list)


def test_live_subnet_list(live_client: NcpClient) -> None:
    result = live_client.vpc.get_subnet_list()
    assert "totalRows" in result
    assert isinstance(result.get("subnetList", []), list)


def test_live_cache_list(live_client: NcpClient) -> None:
    result = live_client.cache.get_cloud_cache_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("cloudCacheInstanceList", []), list)


def test_live_redis_list(live_client: NcpClient) -> None:
    result = live_client.redis.get_cloud_redis_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("cloudRedisInstanceList", []), list)


def test_live_nat_gateway_list(live_client: NcpClient) -> None:
    result = live_client.vpc.get_nat_gateway_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("natGatewayInstanceList", []), list)


def test_live_vpc_peering_list(live_client: NcpClient) -> None:
    result = live_client.vpc.get_vpc_peering_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("vpcPeeringInstanceList", []), list)


def test_live_route_table_list(live_client: NcpClient) -> None:
    result = live_client.vpc.get_route_table_list()
    assert "totalRows" in result
    assert isinstance(result.get("routeTableList", []), list)


def test_live_global_dns_domain_list(live_client: NcpClient) -> None:
    result = live_client.global_dns.get_domain_list()
    assert "totalElements" in result
    assert isinstance(result.get("content", []), list)


def test_live_load_balancer_list(live_client: NcpClient) -> None:
    result = live_client.load_balancer.get_load_balancer_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("loadBalancerInstanceList", []), list)


def test_live_nas_volume_list(live_client: NcpClient) -> None:
    result = live_client.nas.get_nas_volume_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("nasVolumeInstanceList", []), list)


def test_live_object_storage_list_buckets(live_client: NcpClient) -> None:
    result = live_client.object_storage.list_buckets()
    assert "owner" in result
    assert isinstance(result.get("buckets", []), list)


def test_live_object_storage_list_objects(live_client: NcpClient) -> None:
    buckets = live_client.object_storage.list_buckets()["buckets"]
    if not buckets:
        pytest.skip("no buckets in account")
    result = live_client.object_storage.list_objects(buckets[0]["name"], max_keys=10)
    assert "contents" in result
    assert isinstance(result["contents"], list)
    assert isinstance(result["isTruncated"], bool)
