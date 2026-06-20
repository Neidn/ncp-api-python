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
