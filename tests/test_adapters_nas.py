from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.nas import NasApi

BASE_URL = "https://ncloud.apigw.ntruss.com"

SAMPLE_RESPONSE = {
    "getNasVolumeInstanceListResponse": {
        "requestId": "req-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "nasVolumeInstanceList": [
            {
                "nasVolumeInstanceNo": "111111",
                "volumeName": "my-nas",
                "volumeTotalSize": 536870912000,
                "volumeAllotmentProtocolType": {"code": "NFS", "codeName": "NFS"},
                "mountInformation": "10.0.0.1:/my-nas",
                "nasVolumeInstanceStatus": {"code": "CREAT", "codeName": "created"},
                "isSnapshotConfiguration": False,
                "isEventConfiguration": False,
            }
        ],
    }
}


def make_api() -> NasApi:
    from ncp_api.auth import HmacSigner
    return NasApi(BASE_URL, HmacSigner("testkey", "testsecret"))


def test_get_nas_volume_instance_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    result = make_api().get_nas_volume_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
    assert result["nasVolumeInstanceList"][0]["volumeName"] == "my-nas"


def test_get_nas_volume_instance_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_nas_volume_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "/vnas/v2/getNasVolumeInstanceList" in str(sent.url)


def test_get_nas_volume_instance_list_json_format(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_nas_volume_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "responseFormatType=json" in str(sent.url)


def test_get_nas_volume_instance_list_with_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_nas_volume_instance_list(
        region_code="KR",
        zone_code="KR-1",
        volume_name="my-nas",
        volume_allotment_protocol_type_code="NFS",
        is_event_configuration=False,
        is_snapshot_configuration=True,
        page_no=0,
        page_size=10,
        sorted_by="volumeName",
        sorting_order="ASC",
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "regionCode=KR" in url
    assert "zoneCode=KR-1" in url
    assert "volumeName=my-nas" in url
    assert "volumeAllotmentProtocolTypeCode=NFS" in url
    assert "isEventConfiguration=False" in url
    assert "isSnapshotConfiguration=True" in url
    assert "pageNo=0" in url
    assert "pageSize=10" in url
    assert "sortedBy=volumeName" in url
    assert "sortingOrder=ASC" in url


def test_get_nas_volume_instance_no_list_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_nas_volume_instance_list(nas_volume_instance_no_list=["111", "222"])
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "nasVolumeInstanceNoList.1=111" in url
    assert "nasVolumeInstanceNoList.2=222" in url


def test_get_nas_volume_instance_list_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_nas_volume_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


def test_get_nas_volume_instance_list_protocol_cifs(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_nas_volume_instance_list(volume_allotment_protocol_type_code="CIFS")
    sent = httpx_mock.get_requests()[0]
    assert "volumeAllotmentProtocolTypeCode=CIFS" in str(sent.url)


@pytest.mark.asyncio
async def test_aget_nas_volume_instance_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    result = await make_api().aget_nas_volume_instance_list()
    assert isinstance(result, dict)
    assert result["nasVolumeInstanceList"][0]["mountInformation"] == "10.0.0.1:/my-nas"
