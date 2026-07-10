from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.mongodb import CloudMongoDbApi

MONGODB_BASE_URL = "https://ncloud.apigw.ntruss.com"
ENDPOINT_PREFIX = f"{MONGODB_BASE_URL}/vmongodb/v2/getCloudMongoDbInstanceList"

SAMPLE_RESPONSE = {
    "getCloudMongoDbInstanceListResponse": {
        "requestId": "req-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "cloudMongoDbInstanceList": [
            {
                "cloudMongoDbInstanceNo": "222222",
                "cloudMongoDbServiceName": "my-mongo",
                "cloudMongoDbInstanceStatus": {"code": "CREAT", "codeName": "create"},
                "generationCode": "G3",
            }
        ],
    }
}


def make_api() -> CloudMongoDbApi:
    from ncp_api.auth import HmacSigner

    signer = HmacSigner("testkey", "testsecret")
    return CloudMongoDbApi(MONGODB_BASE_URL, signer)


def test_get_cloud_mongodb_instance_list_returns_response(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = api.get_cloud_mongodb_instance_list()
    assert result["totalRows"] == 1
    assert (
        result["cloudMongoDbInstanceList"][0]["cloudMongoDbServiceName"] == "my-mongo"
    )


def test_get_cloud_mongodb_instance_list_sends_get(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_mongodb_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
    assert str(sent.url).startswith(ENDPOINT_PREFIX)


def test_get_cloud_mongodb_instance_list_includes_json_format(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_mongodb_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "responseFormatType=json" in str(sent.url)


def test_get_cloud_mongodb_instance_list_optional_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_mongodb_instance_list(
        vpc_no="456",
        cloud_mongodb_service_name="my-mongo",
        generation_code="G3",
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "vpcNo=456" in url
    assert "cloudMongoDbServiceName=my-mongo" in url
    assert "generationCode=G3" in url


def test_get_cloud_mongodb_instance_list_no_list_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_mongodb_instance_list(cloud_mongodb_instance_no_list=["111", "222"])
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "cloudMongoDbInstanceNoList.1=111" in url
    assert "cloudMongoDbInstanceNoList.2=222" in url


def test_get_cloud_mongodb_instance_list_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_cloud_mongodb_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


@pytest.mark.asyncio
async def test_aget_cloud_mongodb_instance_list_returns_response(
    httpx_mock: Any,
) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = await api.aget_cloud_mongodb_instance_list()
    assert result["totalRows"] == 1
    assert result["cloudMongoDbInstanceList"][0]["cloudMongoDbInstanceNo"] == "222222"


@pytest.mark.asyncio
async def test_aget_cloud_mongodb_instance_list_sends_get(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    await api.aget_cloud_mongodb_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
