from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.nks import NksApi

NKS_BASE_URL = "https://nks.apigw.ntruss.com"

SAMPLE_RESPONSE = {
    "clusters": [
        {
            "name": "my-cluster",
            "status": "RUNNING",
            "k8sVersion": "1.29",
            "nodeCount": 3,
            "endpoint": "https://xxx.kr.clusters.nks.ntruss.com",
            "vpcNo": 12345,
            "regionCode": "KR",
        }
    ]
}

CLUSTER_UUID = "abc-1234-uuid"

SAMPLE_NODES_RESPONSE = {
    "nodes": [
        {
            "id": 1,
            "name": "node-001",
            "serverName": "s-001",
            "privateIp": "10.0.0.1",
            "publicIp": "1.2.3.4",
            "status": "RUNNING",
            "k8sStatus": "Ready",
            "cpuCount": 4,
            "memorySize": 8589934592,
            "nodePoolName": "default",
        }
    ]
}

SAMPLE_NODE_POOL_RESPONSE = {
    "nodePool": [
        {
            "instanceNo": 100,
            "name": "default",
            "nodeCount": "3",
            "k8sVersion": "1.29",
            "status": "RUNNING",
            "zoneCode": "KR-1",
            "productCode": "SVR.VSVR.STAND.C002.M008.NET.SSD050.B050.G002",
        }
    ]
}


def make_api() -> NksApi:
    from ncp_api.auth import HmacSigner
    signer = HmacSigner("testkey", "testsecret")
    return NksApi(NKS_BASE_URL, signer)


def test_get_cluster_list_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = api.get_cluster_list()
    assert isinstance(result, list)
    assert result[0]["name"] == "my-cluster"
    assert result[0]["status"] == "RUNNING"


def test_get_cluster_list_uses_nks_domain(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cluster_list()
    sent = httpx_mock.get_requests()[0]
    assert str(sent.url).startswith(NKS_BASE_URL)


def test_get_cluster_list_default_region_kr(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cluster_list()
    sent = httpx_mock.get_requests()[0]
    assert "/vnks/v2/clusters" in str(sent.url)


def test_get_cluster_list_region_sgn(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cluster_list(region_code="SGN")
    sent = httpx_mock.get_requests()[0]
    assert "/vnks/sgn-v2/clusters" in str(sent.url)


def test_get_cluster_list_region_jpn(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cluster_list(region_code="JPN")
    sent = httpx_mock.get_requests()[0]
    assert "/vnks/jpn-v2/clusters" in str(sent.url)


def test_get_cluster_list_region_krs(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cluster_list(region_code="KRS")
    sent = httpx_mock.get_requests()[0]
    assert "/vnks/krs-v2/clusters" in str(sent.url)


def test_get_cluster_list_region_case_insensitive(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cluster_list(region_code="sgn")
    sent = httpx_mock.get_requests()[0]
    assert "/vnks/sgn-v2/clusters" in str(sent.url)


def test_get_cluster_list_sends_get(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cluster_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"


def test_get_cluster_list_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cluster_list()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


@pytest.mark.asyncio
async def test_aget_cluster_list_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = await api.aget_cluster_list()
    assert isinstance(result, list)
    assert result[0]["k8sVersion"] == "1.29"


@pytest.mark.asyncio
async def test_aget_cluster_list_region_sgn(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    await api.aget_cluster_list(region_code="SGN")
    sent = httpx_mock.get_requests()[0]
    assert "/vnks/sgn-v2/clusters" in str(sent.url)


# --- get_worker_nodes ---

def test_get_worker_nodes_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODES_RESPONSE)
    api = make_api()
    result = api.get_worker_nodes(CLUSTER_UUID)
    assert isinstance(result, list)
    assert result[0]["name"] == "node-001"
    assert result[0]["k8sStatus"] == "Ready"


def test_get_worker_nodes_url_contains_uuid(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODES_RESPONSE)
    api = make_api()
    api.get_worker_nodes(CLUSTER_UUID)
    sent = httpx_mock.get_requests()[0]
    assert f"/vnks/v2/clusters/{CLUSTER_UUID}/nodes" in str(sent.url)


def test_get_worker_nodes_uses_nks_domain(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODES_RESPONSE)
    api = make_api()
    api.get_worker_nodes(CLUSTER_UUID)
    sent = httpx_mock.get_requests()[0]
    assert str(sent.url).startswith(NKS_BASE_URL)


def test_get_worker_nodes_region_sgn(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODES_RESPONSE)
    api = make_api()
    api.get_worker_nodes(CLUSTER_UUID, region_code="SGN")
    sent = httpx_mock.get_requests()[0]
    assert f"/vnks/sgn-v2/clusters/{CLUSTER_UUID}/nodes" in str(sent.url)


@pytest.mark.asyncio
async def test_aget_worker_nodes_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODES_RESPONSE)
    api = make_api()
    result = await api.aget_worker_nodes(CLUSTER_UUID)
    assert isinstance(result, list)
    assert result[0]["cpuCount"] == 4


# --- get_node_pool ---

def test_get_node_pool_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODE_POOL_RESPONSE)
    api = make_api()
    result = api.get_node_pool(CLUSTER_UUID)
    assert isinstance(result, list)
    assert result[0]["name"] == "default"
    assert result[0]["nodeCount"] == "3"


def test_get_node_pool_url_contains_uuid(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODE_POOL_RESPONSE)
    api = make_api()
    api.get_node_pool(CLUSTER_UUID)
    sent = httpx_mock.get_requests()[0]
    assert f"/vnks/v2/clusters/{CLUSTER_UUID}/node-pool" in str(sent.url)


def test_get_node_pool_hypervisor_code_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODE_POOL_RESPONSE)
    api = make_api()
    api.get_node_pool(CLUSTER_UUID, hypervisor_code="KVM")
    sent = httpx_mock.get_requests()[0]
    assert "hypervisorCode=KVM" in str(sent.url)


def test_get_node_pool_no_hypervisor_param_by_default(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODE_POOL_RESPONSE)
    api = make_api()
    api.get_node_pool(CLUSTER_UUID)
    sent = httpx_mock.get_requests()[0]
    assert "hypervisorCode" not in str(sent.url)


def test_get_node_pool_region_jpn(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODE_POOL_RESPONSE)
    api = make_api()
    api.get_node_pool(CLUSTER_UUID, region_code="JPN")
    sent = httpx_mock.get_requests()[0]
    assert f"/vnks/jpn-v2/clusters/{CLUSTER_UUID}/node-pool" in str(sent.url)


@pytest.mark.asyncio
async def test_aget_node_pool_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NODE_POOL_RESPONSE)
    api = make_api()
    result = await api.aget_node_pool(CLUSTER_UUID)
    assert isinstance(result, list)
    assert result[0]["instanceNo"] == 100
