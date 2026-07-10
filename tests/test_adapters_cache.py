from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.cache import CloudCacheApi, CloudRedisApi

BASE_URL = "https://ncloud.apigw.ntruss.com"

SAMPLE_CACHE_RESPONSE = {
    "getCloudCacheInstanceListResponse": {
        "requestId": "req-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "cloudCacheInstanceList": [
            {
                "cloudCacheInstanceNo": "111111",
                "cloudCacheServiceName": "my-cache",
                "cloudCacheDbmsCode": "Redis",
                "generationCode": "G3",
                "cloudCacheInstanceStatus": {"code": "RUNNING", "codeName": "running"},
            }
        ],
    }
}

SAMPLE_REDIS_RESPONSE = {
    "getCloudRedisInstanceListResponse": {
        "requestId": "req-002",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "cloudRedisInstanceList": [
            {
                "cloudRedisInstanceNo": "222222",
                "cloudRedisServiceName": "my-redis",
                "generationCode": "G2",
                "cloudRedisInstanceStatus": {"code": "RUNNING", "codeName": "running"},
            }
        ],
    }
}


def make_cache_api() -> CloudCacheApi:
    from ncp_api.auth import HmacSigner

    return CloudCacheApi(BASE_URL, HmacSigner("testkey", "testsecret"))


def make_redis_api() -> CloudRedisApi:
    from ncp_api.auth import HmacSigner

    return CloudRedisApi(BASE_URL, HmacSigner("testkey", "testsecret"))


# --- CloudCacheApi ---


def test_get_cloud_cache_instance_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_CACHE_RESPONSE)
    result = make_cache_api().get_cloud_cache_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
    assert result["cloudCacheInstanceList"][0]["cloudCacheServiceName"] == "my-cache"


def test_get_cloud_cache_instance_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_CACHE_RESPONSE)
    make_cache_api().get_cloud_cache_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "/vcache/v2/getCloudCacheInstanceList" in str(sent.url)


def test_get_cloud_cache_instance_list_json_format(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_CACHE_RESPONSE)
    make_cache_api().get_cloud_cache_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "responseFormatType=json" in str(sent.url)


def test_get_cloud_cache_instance_list_with_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_CACHE_RESPONSE)
    make_cache_api().get_cloud_cache_instance_list(
        vpc_no="123",
        cloud_cache_service_name="my-cache",
        generation_code="G3",
        cloud_cache_dbms_code="Redis",
        page_no=0,
        page_size=10,
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "vpcNo=123" in url
    assert "cloudCacheServiceName=my-cache" in url
    assert "generationCode=G3" in url
    assert "cloudCacheDbmsCode=Redis" in url
    assert "pageNo=0" in url
    assert "pageSize=10" in url


def test_get_cloud_cache_instance_no_list_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_CACHE_RESPONSE)
    make_cache_api().get_cloud_cache_instance_list(
        cloud_cache_instance_no_list=["111", "222"]
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "cloudCacheInstanceNoList.1=111" in url
    assert "cloudCacheInstanceNoList.2=222" in url


def test_get_cloud_cache_server_instance_no_list_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_CACHE_RESPONSE)
    make_cache_api().get_cloud_cache_instance_list(
        cloud_cache_server_instance_no_list=["aaa", "bbb"]
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "cloudCacheServerInstanceNoList.1=aaa" in url
    assert "cloudCacheServerInstanceNoList.2=bbb" in url


def test_get_cloud_cache_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_CACHE_RESPONSE)
    make_cache_api().get_cloud_cache_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


@pytest.mark.asyncio
async def test_aget_cloud_cache_instance_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_CACHE_RESPONSE)
    result = await make_cache_api().aget_cloud_cache_instance_list()
    assert isinstance(result, dict)
    assert result["cloudCacheInstanceList"][0]["cloudCacheDbmsCode"] == "Redis"


# --- CloudRedisApi ---


def test_get_cloud_redis_instance_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_REDIS_RESPONSE)
    result = make_redis_api().get_cloud_redis_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
    assert result["cloudRedisInstanceList"][0]["cloudRedisServiceName"] == "my-redis"


def test_get_cloud_redis_instance_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_REDIS_RESPONSE)
    make_redis_api().get_cloud_redis_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "/vredis/v2/getCloudRedisInstanceList" in str(sent.url)


def test_get_cloud_redis_instance_list_with_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_REDIS_RESPONSE)
    make_redis_api().get_cloud_redis_instance_list(
        vpc_no="456",
        cloud_redis_service_name="my-redis",
        generation_code="G2",
        page_no=0,
        page_size=5,
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "vpcNo=456" in url
    assert "cloudRedisServiceName=my-redis" in url
    assert "generationCode=G2" in url
    assert "pageNo=0" in url
    assert "pageSize=5" in url


def test_get_cloud_redis_instance_no_list_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_REDIS_RESPONSE)
    make_redis_api().get_cloud_redis_instance_list(
        cloud_redis_instance_no_list=["333", "444"]
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "cloudRedisInstanceNoList.1=333" in url
    assert "cloudRedisInstanceNoList.2=444" in url


@pytest.mark.asyncio
async def test_aget_cloud_redis_instance_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_REDIS_RESPONSE)
    result = await make_redis_api().aget_cloud_redis_instance_list()
    assert isinstance(result, dict)
    assert result["cloudRedisInstanceList"][0]["generationCode"] == "G2"
