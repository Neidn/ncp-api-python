from __future__ import annotations

import json
from typing import Any

import pytest

from ncp_api.adapters.cloud_insight import CloudInsightApi, MetricInfo

CI_BASE_URL = "https://cw.apigw.ntruss.com"
ENDPOINT = "https://cw.apigw.ntruss.com/cw_fea/real/cw/api/data/query/multiple"

SAMPLE_RESPONSE = [
    {
        "aggregation": "AVG",
        "dimensions": {"instanceNo": "12345"},
        "dps": [[1718000000000, 42.5], [1718000060000, 43.1]],
        "interval": "Min1",
        "metric": "cpu_used_rto",
        "productName": "Server",
    }
]

METRIC_INFO = MetricInfo(
    prod_key="cw_key_server",
    metric="cpu_used_rto",
    interval="Min1",
    dimensions={"instanceNo": "12345"},
)


def make_api() -> CloudInsightApi:
    from ncp_api.auth import HmacSigner
    signer = HmacSigner("testkey", "testsecret")
    return CloudInsightApi(CI_BASE_URL, signer)


def test_cloud_insight_uses_injected_domain() -> None:
    api = make_api()
    assert api.base_url == CI_BASE_URL


def test_query_data_multiple_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = api.query_data_multiple(
        time_start=1718000000000,
        time_end=1718003600000,
        metric_info_list=[METRIC_INFO],
    )
    assert isinstance(result, list)
    assert result[0]["metric"] == "cpu_used_rto"
    assert result[0]["dps"] == [[1718000000000, 42.5], [1718000060000, 43.1]]


def test_query_data_multiple_sends_post(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.query_data_multiple(
        time_start=1718000000000,
        time_end=1718003600000,
        metric_info_list=[METRIC_INFO],
    )
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "POST"
    assert str(sent.url) == ENDPOINT


def test_query_data_multiple_request_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.query_data_multiple(
        time_start=1718000000000,
        time_end=1718003600000,
        metric_info_list=[METRIC_INFO],
    )
    sent = httpx_mock.get_requests()[0]
    body = json.loads(sent.content)
    assert body["timeStart"] == 1718000000000
    assert body["timeEnd"] == 1718003600000
    assert len(body["metricInfoList"]) == 1
    m = body["metricInfoList"][0]
    assert m["prodKey"] == "cw_key_server"
    assert m["metric"] == "cpu_used_rto"
    assert m["interval"] == "Min1"
    assert m["dimensions"] == {"instanceNo": "12345"}
    assert m["aggregation"] == "AVG"
    assert "queryAggregation" not in m


def test_query_data_multiple_with_query_aggregation(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    metric = MetricInfo(
        prod_key="cw_key_server",
        metric="cpu_used_rto",
        interval="Min5",
        dimensions={"instanceNo": "12345"},
        aggregation="MAX",
        query_aggregation="SUM",
    )
    api.query_data_multiple(
        time_start=1718000000000,
        time_end=1718003600000,
        metric_info_list=[metric],
    )
    sent = httpx_mock.get_requests()[0]
    body = json.loads(sent.content)
    m = body["metricInfoList"][0]
    assert m["aggregation"] == "MAX"
    assert m["queryAggregation"] == "SUM"
    assert m["interval"] == "Min5"


def test_query_data_multiple_multiple_metrics(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE * 2)
    api = make_api()
    metrics = [
        MetricInfo(prod_key="k1", metric="cpu_used_rto", interval="Min1", dimensions={"instanceNo": "1"}),
        MetricInfo(prod_key="k2", metric="mem_usert", interval="Min5", dimensions={"instanceNo": "2"}),
    ]
    api.query_data_multiple(
        time_start=1718000000000,
        time_end=1718003600000,
        metric_info_list=metrics,
    )
    sent = httpx_mock.get_requests()[0]
    body = json.loads(sent.content)
    assert len(body["metricInfoList"]) == 2


def test_query_data_multiple_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.query_data_multiple(
        time_start=1718000000000,
        time_end=1718003600000,
        metric_info_list=[METRIC_INFO],
    )
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


@pytest.mark.asyncio
async def test_aquery_data_multiple_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = await api.aquery_data_multiple(
        time_start=1718000000000,
        time_end=1718003600000,
        metric_info_list=[METRIC_INFO],
    )
    assert isinstance(result, list)
    assert result[0]["metric"] == "cpu_used_rto"


@pytest.mark.asyncio
async def test_aquery_data_multiple_sends_post(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    await api.aquery_data_multiple(
        time_start=1718000000000,
        time_end=1718003600000,
        metric_info_list=[METRIC_INFO],
    )
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "POST"


SERVERS_TOP_RESPONSE = [
    {
        "avg_cpu_user_rto": "0.34282196",
        "hostName": "server-01",
        "instanceNo": "12345",
        "avg_cpu_used_rto": 0.34282196,
        "avg_fs_usert": 8.1264,
        "mem_usert": 4.8596377,
    },
    {
        "avg_cpu_user_rto": "0.3427846",
        "hostName": "server-02",
        "instanceNo": "12346",
        "avg_cpu_used_rto": 0.3427846,
        "avg_fs_usert": 8.132111,
        "mem_usert": 4.678288,
    },
]


def test_get_servers_top_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SERVERS_TOP_RESPONSE)
    api = make_api()
    result = api.get_servers_top(query="avg_cpu_used_rto")
    assert isinstance(result, list)
    assert result[0]["hostName"] == "server-01"
    assert result[0]["avg_cpu_used_rto"] == 0.34282196


def test_get_servers_top_sends_post_with_query_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SERVERS_TOP_RESPONSE)
    api = make_api()
    api.get_servers_top(query="avg_cpu_used_rto")
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "POST"
    assert "query=avg_cpu_used_rto" in str(sent.url)
    assert str(sent.url).startswith(
        f"{CI_BASE_URL}/cw_fea/real/cw/api/servers/top"
    )


def test_get_servers_top_with_prod_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SERVERS_TOP_RESPONSE)
    api = make_api()
    api.get_servers_top(query="mem_usert", prod="Classic")
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "query=mem_usert" in url
    assert "prod=Classic" in url


def test_get_servers_top_without_prod_omits_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SERVERS_TOP_RESPONSE)
    api = make_api()
    api.get_servers_top(query="avg_fs_usert")
    sent = httpx_mock.get_requests()[0]
    assert "prod" not in str(sent.url)


@pytest.mark.asyncio
async def test_aget_servers_top_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SERVERS_TOP_RESPONSE)
    api = make_api()
    result = await api.aget_servers_top(query="avg_cpu_used_rto")
    assert isinstance(result, list)
    assert result[0]["instanceNo"] == "12345"


# --- get_system_schema_key_list ---

SCHEMA_KEY_LIST_RESPONSE = [
    {"cw_key": "NCPObjectStorage", "prodName": "Object Storage"},
    {"cw_key": "NCPLoadBalancer", "prodName": "Load Balancer Monitor(VPC)"},
]


def test_get_system_schema_key_list_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SCHEMA_KEY_LIST_RESPONSE)
    api = make_api()
    result = api.get_system_schema_key_list()
    assert isinstance(result, list)
    assert result[0]["cw_key"] == "NCPObjectStorage"
    assert result[0]["prodName"] == "Object Storage"


def test_get_system_schema_key_list_sends_get(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SCHEMA_KEY_LIST_RESPONSE)
    api = make_api()
    api.get_system_schema_key_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"


def test_get_system_schema_key_list_correct_url(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SCHEMA_KEY_LIST_RESPONSE)
    api = make_api()
    api.get_system_schema_key_list()
    sent = httpx_mock.get_requests()[0]
    assert str(sent.url).startswith(f"{CI_BASE_URL}/cw_fea/real/cw/api/schema/system/list")


@pytest.mark.asyncio
async def test_aget_system_schema_key_list_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SCHEMA_KEY_LIST_RESPONSE)
    api = make_api()
    result = await api.aget_system_schema_key_list()
    assert isinstance(result, list)
    assert result[1]["prodName"] == "Load Balancer Monitor(VPC)"
