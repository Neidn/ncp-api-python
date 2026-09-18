from __future__ import annotations

from typing import Any

from ncp_api.adapters.cloud_log_analytics import CloudLogAnalyticsApi
from ncp_api.auth import HmacSigner

BASE_URL = "https://cloudloganalytics.apigw.ntruss.com"

SERVER_RESPONSE = {
    "code": 0,
    "message": "success",
    "result": {
        "pageSize": 10,
        "currentPage": 1,
        "totalPage": 1,
        "totalCount": 1,
        "isPaged": True,
        "vpcServerInfos": [{"additionalParameterMap": {}}],
        "collectingCount": 1,
    },
}

DB_RESPONSE = {
    "code": 0,
    "message": "success",
    "result": {
        "pageSize": 20,
        "currentPage": 1,
        "totalPage": 1,
        "totalCount": 1,
        "isPaged": True,
        "dbServers": [{"serverName": "db-01"}],
    },
}

CLUSTER_RESPONSE = {
    "code": 0,
    "message": "success",
    "result": {
        "pageSize": 20,
        "currentPage": 1,
        "totalPage": 1,
        "totalCount": 1,
        "isPaged": True,
        "clusters": [{"clusterName": "cluster-01"}],
    },
}


def make_api() -> CloudLogAnalyticsApi:
    return CloudLogAnalyticsApi(BASE_URL, HmacSigner("testkey", "testsecret"))


def test_get_vpc_server_list_path_and_result(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SERVER_RESPONSE)
    result = make_api().get_vpc_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers" in str(sent.url)
    assert result["vpcServerInfos"] == [{"additionalParameterMap": {}}]
    assert result["collectingCount"] == 1


def test_get_vpc_server_list_pagination_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SERVER_RESPONSE)
    make_api().get_vpc_server_list(region_code="kr", page_no=2, page_size=50)
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "pageNo=2" in url
    assert "pageSize=50" in url


async def test_aget_vpc_server_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SERVER_RESPONSE)
    result = await make_api().aget_vpc_server_list(region_code="kr")
    assert isinstance(result, dict)
    assert result["collectingCount"] == 1


def test_get_vpc_mysql_server_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=DB_RESPONSE)
    result = make_api().get_vpc_mysql_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers/mysql" in str(sent.url)
    assert result["dbServers"][0]["serverName"] == "db-01"


async def test_aget_vpc_mysql_server_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=DB_RESPONSE)
    await make_api().aget_vpc_mysql_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers/mysql" in str(sent.url)


def test_get_vpc_mssql_server_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=DB_RESPONSE)
    make_api().get_vpc_mssql_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers/mssql" in str(sent.url)


def test_get_vpc_mongodb_server_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=DB_RESPONSE)
    make_api().get_vpc_mongodb_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers/mongodb" in str(sent.url)


def test_get_vpc_postgresql_server_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=DB_RESPONSE)
    make_api().get_vpc_postgresql_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers/postgresql" in str(sent.url)


def test_get_vpc_baremetal_server_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=DB_RESPONSE)
    make_api().get_vpc_baremetal_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers/baremetal" in str(sent.url)


def test_get_vpc_nks_server_list_path_uses_kubernetes_slug(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_RESPONSE)
    result = make_api().get_vpc_nks_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers/kubernetes" in str(sent.url)
    assert result["clusters"][0]["clusterName"] == "cluster-01"


async def test_aget_vpc_nks_server_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_RESPONSE)
    await make_api().aget_vpc_nks_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers/kubernetes" in str(sent.url)


def test_get_vpc_ses_server_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_RESPONSE)
    make_api().get_vpc_ses_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers/ses" in str(sent.url)


def test_get_vpc_cdss_server_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_RESPONSE)
    make_api().get_vpc_cdss_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "/api/kr-v1/vpc/servers/cdss" in str(sent.url)


def test_get_vpc_server_list_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SERVER_RESPONSE)
    make_api().get_vpc_server_list(region_code="kr")
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers
