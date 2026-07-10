from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.block_storage import BlockStorageApi

BASE_URL = "https://ncloud.apigw.ntruss.com"

SAMPLE_RESPONSE = {
    "getBlockStorageInstanceListResponse": {
        "requestId": "req-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "blockStorageInstanceList": [
            {
                "blockStorageInstanceNo": "555555",
                "blockStorageName": "my-disk",
                "blockStorageSize": 107374182400,
                "blockStorageTypeCode": "BASIC",
                "blockStorageStatusCode": "ATTAC",
                "serverInstanceNo": "140599555",
                "serverName": "my-server",
                "deviceName": "/dev/xvdb",
            }
        ],
    }
}


def make_api() -> BlockStorageApi:
    from ncp_api.auth import HmacSigner

    signer = HmacSigner("testkey", "testsecret")
    return BlockStorageApi(BASE_URL, signer)


def test_get_block_storage_instance_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = api.get_block_storage_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
    assert result["blockStorageInstanceList"][0]["blockStorageName"] == "my-disk"


def test_get_block_storage_instance_list_sends_get(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_block_storage_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"


def test_get_block_storage_instance_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_block_storage_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "/vserver/v2/getBlockStorageInstanceList" in str(sent.url)


def test_get_block_storage_instance_list_json_format(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_block_storage_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "responseFormatType=json" in str(sent.url)


def test_get_block_storage_instance_list_with_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_block_storage_instance_list(
        region_code="KR",
        block_storage_name="my-disk",
        block_storage_type_code="BASIC",
        block_storage_status_code="ATTAC",
        server_instance_no="140599555",
        page_no=0,
        page_size=10,
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "regionCode=KR" in url
    assert "blockStorageName=my-disk" in url
    assert "blockStorageTypeCode=BASIC" in url
    assert "blockStorageStatusCode=ATTAC" in url
    assert "serverInstanceNo=140599555" in url
    assert "pageNo=0" in url
    assert "pageSize=10" in url


def test_get_block_storage_instance_no_list_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_block_storage_instance_list(block_storage_instance_no_list=["111", "222"])
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "blockStorageInstanceNoList.1=111" in url
    assert "blockStorageInstanceNoList.2=222" in url


def test_get_block_storage_instance_list_disk_type_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_block_storage_instance_list(
        block_storage_disk_type_code="NET",
        block_storage_disk_detail_type_code="SSD",
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "blockStorageDiskTypeCode=NET" in url
    assert "blockStorageDiskDetailTypeCode=SSD" in url


def test_get_block_storage_instance_list_sort_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_block_storage_instance_list(
        sorted_by="blockStorageName", sorting_order="ASC"
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "sortedBy=blockStorageName" in url
    assert "sortingOrder=ASC" in url


def test_get_block_storage_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    api.get_block_storage_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


@pytest.mark.asyncio
async def test_aget_block_storage_instance_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    api = make_api()
    result = await api.aget_block_storage_instance_list()
    assert isinstance(result, dict)
    assert result["blockStorageInstanceList"][0]["blockStorageStatusCode"] == "ATTAC"
