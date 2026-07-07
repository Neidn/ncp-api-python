from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.mysql import CloudMysqlApi

MYSQL_BASE_URL = "https://ncloud.apigw.ntruss.com"
ENDPOINT_PREFIX = f"{MYSQL_BASE_URL}/vmysql/v2/getCloudMysqlInstanceList"

SAMPLE_RESPONSE = {
    "getCloudMysqlInstanceListResponse": {
        "requestId": "req-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "cloudMysqlInstanceList": [
            {
                "cloudMysqlInstanceNo": "111111",
                "cloudMysqlServiceName": "my-db",
                "cloudMysqlInstanceStatus": {"code": "CREAT", "codeName": "create"},
                "generationCode": "G2",
            }
        ],
    }
}


def make_api() -> CloudMysqlApi:
    from ncp_api.auth import HmacSigner
    signer = HmacSigner("testkey", "testsecret")
    return CloudMysqlApi(MYSQL_BASE_URL, signer)


def test_get_cloud_mysql_instance_list_returns_response(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = api.get_cloud_mysql_instance_list()
    assert result["totalRows"] == 1
    assert result["cloudMysqlInstanceList"][0]["cloudMysqlServiceName"] == "my-db"


def test_get_cloud_mysql_instance_list_sends_get(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_mysql_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
    assert str(sent.url).startswith(ENDPOINT_PREFIX)


def test_get_cloud_mysql_instance_list_includes_json_format(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_mysql_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "responseFormatType=json" in str(sent.url)


def test_get_cloud_mysql_instance_list_optional_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_mysql_instance_list(
        vpc_no="123",
        cloud_mysql_service_name="my-db",
        generation_code="G2",
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "vpcNo=123" in url
    assert "cloudMysqlServiceName=my-db" in url
    assert "generationCode=G2" in url


def test_get_cloud_mysql_instance_list_no_list_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_mysql_instance_list(cloud_mysql_instance_no_list=["111", "222"])
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "cloudMysqlInstanceNoList.1=111" in url
    assert "cloudMysqlInstanceNoList.2=222" in url


def test_get_cloud_mysql_instance_list_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_mysql_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


@pytest.mark.asyncio
async def test_aget_cloud_mysql_instance_list_returns_response(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = await api.aget_cloud_mysql_instance_list()
    assert result["totalRows"] == 1
    assert result["cloudMysqlInstanceList"][0]["cloudMysqlInstanceNo"] == "111111"


@pytest.mark.asyncio
async def test_aget_cloud_mysql_instance_list_sends_get(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    await api.aget_cloud_mysql_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
