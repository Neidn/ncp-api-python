from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.vpc import VpcApi

BASE_URL = "https://ncloud.apigw.ntruss.com"

SAMPLE_VPC_RESPONSE = {
    "getVpcListResponse": {
        "requestId": "req-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "vpcList": [
            {
                "vpcNo": "12345",
                "vpcName": "my-vpc",
                "ipv4CidrBlock": "10.0.0.0/16",
                "vpcStatusCode": "RUN",
                "regionCode": "KR",
            }
        ],
    }
}

SAMPLE_SUBNET_RESPONSE = {
    "getSubnetListResponse": {
        "requestId": "req-002",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "subnetList": [
            {
                "subnetNo": "99999",
                "subnetName": "my-subnet",
                "subnet": "10.0.1.0/24",
                "subnetStatusCode": "RUN",
                "vpcNo": "12345",
                "zoneCode": "KR-1",
                "subnetTypeCode": "PUBLIC",
                "usageTypeCode": "GEN",
            }
        ],
    }
}


def make_api() -> VpcApi:
    from ncp_api.auth import HmacSigner
    signer = HmacSigner("testkey", "testsecret")
    return VpcApi(BASE_URL, signer)


# --- get_vpc_list ---

def test_get_vpc_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_RESPONSE)
    api = make_api()
    result = api.get_vpc_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
    assert result["vpcList"][0]["vpcName"] == "my-vpc"


def test_get_vpc_list_sends_get(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_RESPONSE)
    api = make_api()
    api.get_vpc_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"


def test_get_vpc_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_RESPONSE)
    api = make_api()
    api.get_vpc_list()
    sent = httpx_mock.get_requests()[0]
    assert "/vpc/v2/getVpcList" in str(sent.url)


def test_get_vpc_list_json_format(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_RESPONSE)
    api = make_api()
    api.get_vpc_list()
    sent = httpx_mock.get_requests()[0]
    assert "responseFormatType=json" in str(sent.url)


def test_get_vpc_list_with_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_RESPONSE)
    api = make_api()
    api.get_vpc_list(vpc_name="my-vpc", vpc_status_code="RUN")
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "vpcName=my-vpc" in url
    assert "vpcStatusCode=RUN" in url


def test_get_vpc_list_no_list_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_RESPONSE)
    api = make_api()
    api.get_vpc_list(vpc_no_list=["111", "222"])
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "vpcNoList.1=111" in url
    assert "vpcNoList.2=222" in url


def test_get_vpc_list_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_RESPONSE)
    api = make_api()
    api.get_vpc_list()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


@pytest.mark.asyncio
async def test_aget_vpc_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_RESPONSE)
    api = make_api()
    result = await api.aget_vpc_list()
    assert isinstance(result, dict)
    assert result["vpcList"][0]["ipv4CidrBlock"] == "10.0.0.0/16"


# --- get_subnet_list ---

def test_get_subnet_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_SUBNET_RESPONSE)
    api = make_api()
    result = api.get_subnet_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
    assert result["subnetList"][0]["subnetName"] == "my-subnet"


def test_get_subnet_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_SUBNET_RESPONSE)
    api = make_api()
    api.get_subnet_list()
    sent = httpx_mock.get_requests()[0]
    assert "/vpc/v2/getSubnetList" in str(sent.url)


def test_get_subnet_list_with_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_SUBNET_RESPONSE)
    api = make_api()
    api.get_subnet_list(
        vpc_no="12345",
        zone_code="KR-1",
        subnet_type_code="PUBLIC",
        usage_type_code="GEN",
        subnet_name="my-subnet",
        subnet="10.0.1.0/24",
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "vpcNo=12345" in url
    assert "zoneCode=KR-1" in url
    assert "subnetTypeCode=PUBLIC" in url
    assert "usageTypeCode=GEN" in url
    assert "subnetName=my-subnet" in url


def test_get_subnet_list_no_list_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_SUBNET_RESPONSE)
    api = make_api()
    api.get_subnet_list(subnet_no_list=["111", "222"])
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "subnetNoList.1=111" in url
    assert "subnetNoList.2=222" in url


def test_get_subnet_list_network_acl_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_SUBNET_RESPONSE)
    api = make_api()
    api.get_subnet_list(network_acl_no="777")
    sent = httpx_mock.get_requests()[0]
    assert "networkAclNo=777" in str(sent.url)


def test_get_subnet_list_pagination_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_SUBNET_RESPONSE)
    api = make_api()
    api.get_subnet_list(page_no=0, page_size=20)
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "pageNo=0" in url
    assert "pageSize=20" in url


@pytest.mark.asyncio
async def test_aget_subnet_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_SUBNET_RESPONSE)
    api = make_api()
    result = await api.aget_subnet_list()
    assert isinstance(result, dict)
    assert result["subnetList"][0]["subnetTypeCode"] == "PUBLIC"
