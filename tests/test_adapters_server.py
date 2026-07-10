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
    await api.aget_server_instance_list(
        server_name="async-server", page_no=0, page_size=5
    )
    sent = httpx_mock.get_requests()[0]
    url_str = str(sent.url)
    assert "serverName=async-server" in url_str
    assert "pageNo=0" in url_str
    assert "pageSize=5" in url_str


# --- get_public_ip_instance_list ---

SAMPLE_PUBLIC_IP_RESPONSE = {
    "getPublicIpInstanceListResponse": {
        "requestId": "req-pip-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 2,
        "publicIpInstanceList": [
            {
                "publicIpInstanceNo": "111",
                "publicIp": "1.2.3.4",
                "publicIpKindTypeCode": "GEN",
                "serverInstanceAssociatedWithPublicIp": {
                    "serverInstanceNo": "999",
                    "serverName": "my-server",
                },
            },
            {
                "publicIpInstanceNo": "222",
                "publicIp": "5.6.7.8",
                "publicIpKindTypeCode": "GEN",
                "serverInstanceAssociatedWithPublicIp": None,
            },
        ],
    }
}

EMPTY_PUBLIC_IP_RESPONSE = {
    "getPublicIpInstanceListResponse": {
        "requestId": "req-pip-002",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 0,
        "publicIpInstanceList": [],
    }
}


def make_server_api() -> ServerApi:  # type: ignore[no-redef]
    return ServerApi(BASE_URL, HmacSigner("testkey", "testsecret"))


def test_get_public_ip_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    result = make_server_api().get_public_ip_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 2


def test_get_public_ip_list_instance_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    result = make_server_api().get_public_ip_instance_list()
    pip_list = result["publicIpInstanceList"]
    assert len(pip_list) == 2
    assert pip_list[0]["publicIp"] == "1.2.3.4"
    assert pip_list[1]["publicIp"] == "5.6.7.8"


def test_get_public_ip_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    make_server_api().get_public_ip_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
    assert "/vserver/v2/getPublicIpInstanceList" in str(sent.url)


def test_get_public_ip_list_is_associated_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    make_server_api().get_public_ip_instance_list(is_associated=True)
    sent = httpx_mock.get_requests()[0]
    assert "isAssociated=True" in str(sent.url)


def test_get_public_ip_list_public_ip_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    make_server_api().get_public_ip_instance_list(public_ip="1.2.3.4")
    sent = httpx_mock.get_requests()[0]
    assert "publicIp=1.2.3.4" in str(sent.url)


def test_get_public_ip_list_kind_type_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    make_server_api().get_public_ip_instance_list(public_ip_kind_type_code="GEN")
    sent = httpx_mock.get_requests()[0]
    assert "publicIpKindTypeCode=GEN" in str(sent.url)


def test_get_public_ip_list_server_instance_no_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    make_server_api().get_public_ip_instance_list(server_instance_no="999")
    sent = httpx_mock.get_requests()[0]
    assert "serverInstanceNo=999" in str(sent.url)


def test_get_public_ip_list_instance_no_list_indexed(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    make_server_api().get_public_ip_instance_list(
        public_ip_instance_no_list=["111", "222"]
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "publicIpInstanceNoList.1=111" in url
    assert "publicIpInstanceNoList.2=222" in url


def test_get_public_ip_list_pagination_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    make_server_api().get_public_ip_instance_list(page_no=1, page_size=10)
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "pageNo=1" in url
    assert "pageSize=10" in url


def test_get_public_ip_list_sorting_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    make_server_api().get_public_ip_instance_list(
        sorted_by="publicIp", sorting_order="ASC"
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "sortedBy=publicIp" in url
    assert "sortingOrder=ASC" in url


def test_get_public_ip_list_empty(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=EMPTY_PUBLIC_IP_RESPONSE)
    result = make_server_api().get_public_ip_instance_list()
    assert result["totalRows"] == 0
    assert result["publicIpInstanceList"] == []


async def test_aget_public_ip_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_PUBLIC_IP_RESPONSE)
    result = await make_server_api().aget_public_ip_instance_list()
    assert isinstance(result, dict)
    assert result["publicIpInstanceList"][0]["publicIp"] == "1.2.3.4"
