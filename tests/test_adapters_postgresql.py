from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.postgresql import CloudPostgresqlApi

BASE_URL = "https://ncloud.apigw.ntruss.com"

SAMPLE_RESPONSE = {
    "getCloudPostgresqlInstanceListResponse": {
        "requestId": "req-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "cloudPostgresqlInstanceList": [
            {
                "cloudPostgresqlInstanceNo": "111111",
                "cloudPostgresqlServiceName": "my-postgres",
                "isHa": True,
                "isMultiZone": False,
                "cloudPostgresqlInstanceStatus": {
                    "code": "RUNNING",
                    "codeName": "running",
                },
            }
        ],
    }
}


def make_api() -> CloudPostgresqlApi:
    from ncp_api.auth import HmacSigner

    signer = HmacSigner("testkey", "testsecret")
    return CloudPostgresqlApi(BASE_URL, signer)


def test_get_cloud_postgresql_instance_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = api.get_cloud_postgresql_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
    assert (
        result["cloudPostgresqlInstanceList"][0]["cloudPostgresqlServiceName"]
        == "my-postgres"
    )


def test_get_cloud_postgresql_instance_list_sends_get(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_postgresql_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"


def test_get_cloud_postgresql_instance_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_postgresql_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "/vpostgresql/v2/getCloudPostgresqlInstanceList" in str(sent.url)


def test_get_cloud_postgresql_instance_list_json_format(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_postgresql_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "responseFormatType=json" in str(sent.url)


def test_get_cloud_postgresql_instance_list_with_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_postgresql_instance_list(
        vpc_no="123",
        cloud_postgresql_service_name="my-postgres",
        page_no=0,
        page_size=10,
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "vpcNo=123" in url
    assert "cloudPostgresqlServiceName=my-postgres" in url
    assert "pageNo=0" in url
    assert "pageSize=10" in url


def test_get_cloud_postgresql_instance_no_list_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_postgresql_instance_list(
        cloud_postgresql_instance_no_list=["111", "222"]
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "cloudPostgresqlInstanceNoList.1=111" in url
    assert "cloudPostgresqlInstanceNoList.2=222" in url


def test_get_cloud_postgresql_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_postgresql_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


@pytest.mark.asyncio
async def test_aget_cloud_postgresql_instance_list_returns_dict(
    httpx_mock: Any,
) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = await api.aget_cloud_postgresql_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
