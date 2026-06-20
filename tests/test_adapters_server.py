from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.server import ServerApi
from ncp_api.auth import HmacSigner

BASE_URL = "https://ncloud.apigw.ntruss.com"
ENDPOINT = "https://ncloud.apigw.ntruss.com/vserver/v2/getServerInstanceList"

SAMPLE_RESPONSE = {
    "getServerInstanceListResponse": {
        "requestId": "abc-123",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "serverInstanceList": [
            {
                "serverInstanceNo": "12345",
                "serverName": "test-server",
                "cpuCount": 2,
                "memorySize": 4294967296,
                "serverInstanceStatusCode": "RUN",
            }
        ],
    }
}


def make_server_api() -> ServerApi:
    signer = HmacSigner("testkey", "testsecret")
    return ServerApi(BASE_URL, signer)


def test_get_server_instance_list_returns_inner_response(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_server_api()
    result = api.get_server_instance_list()
    assert result["returnCode"] == "0"
    assert result["totalRows"] == 1
    assert result["serverInstanceList"][0]["serverName"] == "test-server"


def test_get_server_instance_list_no_filter_sends_only_format_param(
    httpx_mock: Any,
) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_server_api()
    api.get_server_instance_list()
    sent = httpx_mock.get_requests()[0]
    url_str = str(sent.url)
    assert f"{ENDPOINT}?" in url_str
    assert "responseFormatType=json" in url_str
    assert "serverName" not in url_str


def test_get_server_instance_list_with_server_name(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_server_api()
    api.get_server_instance_list(server_name="my-server")
    sent = httpx_mock.get_requests()[0]
    assert "serverName=my-server" in str(sent.url)


def test_get_server_instance_list_with_status_code(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_server_api()
    api.get_server_instance_list(server_instance_status_code="RUN")
    sent = httpx_mock.get_requests()[0]
    assert "serverInstanceStatusCode=RUN" in str(sent.url)


def test_get_server_instance_list_with_pagination(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_server_api()
    api.get_server_instance_list(page_no=1, page_size=10)
    sent = httpx_mock.get_requests()[0]
    assert "pageNo=1" in str(sent.url)
    assert "pageSize=10" in str(sent.url)


def test_get_server_instance_list_array_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_server_api()
    api.get_server_instance_list(server_instance_no_list=["111", "222"])
    sent = httpx_mock.get_requests()[0]
    url_str = str(sent.url)
    assert "serverInstanceNoList.1=111" in url_str
    assert "serverInstanceNoList.2=222" in url_str


def test_get_server_instance_list_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_server_api()
    api.get_server_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


@pytest.mark.asyncio
async def test_aget_server_instance_list_returns_inner_response(
    httpx_mock: Any,
) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_server_api()
    result = await api.aget_server_instance_list()
    assert result["returnCode"] == "0"
    assert result["totalRows"] == 1


@pytest.mark.asyncio
async def test_aget_server_instance_list_with_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_server_api()
    await api.aget_server_instance_list(server_name="async-server", page_no=0, page_size=5)
    sent = httpx_mock.get_requests()[0]
    url_str = str(sent.url)
    assert "serverName=async-server" in url_str
    assert "pageNo=0" in url_str
    assert "pageSize=5" in url_str
