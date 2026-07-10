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


# --- get_nat_gateway_instance_list ---

SAMPLE_NAT_GATEWAY_RESPONSE = {
    "getNatGatewayInstanceListResponse": {
        "requestId": "req-003",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "natGatewayInstanceList": [
            {
                "natGatewayInstanceNo": "55555",
                "natGatewayName": "my-nat",
                "natGatewayStatusCode": "RUN",
                "vpcNo": "12345",
                "subnetNo": "99999",
                "publicIpInstanceNo": "44444",
                "publicIp": "1.2.3.4",
            }
        ],
    }
}

EMPTY_NAT_GATEWAY_RESPONSE = {
    "getNatGatewayInstanceListResponse": {
        "requestId": "req-004",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 0,
        "natGatewayInstanceList": [],
    }
}


def test_get_nat_gateway_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    result = make_api().get_nat_gateway_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1


def test_get_nat_gateway_list_instance_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    result = make_api().get_nat_gateway_instance_list()
    gw_list = result["natGatewayInstanceList"]
    assert len(gw_list) == 1
    assert gw_list[0]["natGatewayName"] == "my-nat"
    assert gw_list[0]["publicIp"] == "1.2.3.4"


def test_get_nat_gateway_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    make_api().get_nat_gateway_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
    assert "/vpc/v2/getNatGatewayInstanceList" in str(sent.url)


def test_get_nat_gateway_list_region_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    make_api().get_nat_gateway_instance_list(region_code="KR")
    sent = httpx_mock.get_requests()[0]
    assert "regionCode=KR" in str(sent.url)


def test_get_nat_gateway_list_name_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    make_api().get_nat_gateway_instance_list(nat_gateway_name="my-nat")
    sent = httpx_mock.get_requests()[0]
    assert "natGatewayName=my-nat" in str(sent.url)


def test_get_nat_gateway_list_status_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    make_api().get_nat_gateway_instance_list(nat_gateway_status_code="RUN")
    sent = httpx_mock.get_requests()[0]
    assert "natGatewayStatusCode=RUN" in str(sent.url)


def test_get_nat_gateway_list_vpc_no_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    make_api().get_nat_gateway_instance_list(vpc_no="12345")
    sent = httpx_mock.get_requests()[0]
    assert "vpcNo=12345" in str(sent.url)


def test_get_nat_gateway_list_subnet_no_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    make_api().get_nat_gateway_instance_list(subnet_no="99999")
    sent = httpx_mock.get_requests()[0]
    assert "subnetNo=99999" in str(sent.url)


def test_get_nat_gateway_list_instance_no_list_indexed(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    make_api().get_nat_gateway_instance_list(nat_gateway_instance_no_list=["55555", "66666"])
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "natGatewayInstanceNoList.1=55555" in url
    assert "natGatewayInstanceNoList.2=66666" in url


def test_get_nat_gateway_list_pagination_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    make_api().get_nat_gateway_instance_list(page_no=1, page_size=20)
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "pageNo=1" in url
    assert "pageSize=20" in url


def test_get_nat_gateway_list_sorting_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    make_api().get_nat_gateway_instance_list(sorted_by="natGatewayName", sorting_order="DESC")
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "sortedBy=natGatewayName" in url
    assert "sortingOrder=DESC" in url


def test_get_nat_gateway_list_empty(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=EMPTY_NAT_GATEWAY_RESPONSE)
    result = make_api().get_nat_gateway_instance_list()
    assert result["totalRows"] == 0
    assert result["natGatewayInstanceList"] == []


@pytest.mark.asyncio
async def test_aget_nat_gateway_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_NAT_GATEWAY_RESPONSE)
    result = await make_api().aget_nat_gateway_instance_list()
    assert isinstance(result, dict)
    assert result["natGatewayInstanceList"][0]["natGatewayName"] == "my-nat"


# --- get_vpc_peering_instance_list ---

SAMPLE_VPC_PEERING_RESPONSE = {
    "getVpcPeeringInstanceListResponse": {
        "requestId": "req-peer-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "vpcPeeringInstanceList": [
            {
                "vpcPeeringInstanceNo": "77777",
                "vpcPeeringName": "my-peering",
                "vpcPeeringStatusCode": "RUN",
                "sourceVpcNo": "12345",
                "sourceVpcName": "vpc-a",
                "targetVpcNo": "67890",
                "targetVpcName": "vpc-b",
            }
        ],
    }
}

EMPTY_VPC_PEERING_RESPONSE = {
    "getVpcPeeringInstanceListResponse": {
        "requestId": "req-peer-002",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 0,
        "vpcPeeringInstanceList": [],
    }
}


def test_get_vpc_peering_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    result = make_api().get_vpc_peering_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1


def test_get_vpc_peering_list_instance_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    result = make_api().get_vpc_peering_instance_list()
    peer_list = result["vpcPeeringInstanceList"]
    assert len(peer_list) == 1
    assert peer_list[0]["vpcPeeringName"] == "my-peering"
    assert peer_list[0]["sourceVpcNo"] == "12345"
    assert peer_list[0]["targetVpcNo"] == "67890"


def test_get_vpc_peering_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    make_api().get_vpc_peering_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
    assert "/vpc/v2/getVpcPeeringInstanceList" in str(sent.url)


def test_get_vpc_peering_list_name_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    make_api().get_vpc_peering_instance_list(vpc_peering_name="my-peering")
    sent = httpx_mock.get_requests()[0]
    assert "vpcPeeringName=my-peering" in str(sent.url)


def test_get_vpc_peering_list_status_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    make_api().get_vpc_peering_instance_list(vpc_peering_status_code="RUN")
    sent = httpx_mock.get_requests()[0]
    assert "vpcPeeringStatusCode=RUN" in str(sent.url)


def test_get_vpc_peering_list_source_vpc_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    make_api().get_vpc_peering_instance_list(source_vpc_no="12345")
    sent = httpx_mock.get_requests()[0]
    assert "sourceVpcNo=12345" in str(sent.url)


def test_get_vpc_peering_list_target_vpc_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    make_api().get_vpc_peering_instance_list(target_vpc_no="67890")
    sent = httpx_mock.get_requests()[0]
    assert "targetVpcNo=67890" in str(sent.url)


def test_get_vpc_peering_list_instance_no_list_indexed(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    make_api().get_vpc_peering_instance_list(vpc_peering_instance_no_list=["77777", "88888"])
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "vpcPeeringInstanceNoList.1=77777" in url
    assert "vpcPeeringInstanceNoList.2=88888" in url


def test_get_vpc_peering_list_pagination_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    make_api().get_vpc_peering_instance_list(page_no=2, page_size=5)
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "pageNo=2" in url
    assert "pageSize=5" in url


def test_get_vpc_peering_list_sorting_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    make_api().get_vpc_peering_instance_list(sorted_by="vpcPeeringName", sorting_order="ASC")
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "sortedBy=vpcPeeringName" in url
    assert "sortingOrder=ASC" in url


def test_get_vpc_peering_list_empty(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=EMPTY_VPC_PEERING_RESPONSE)
    result = make_api().get_vpc_peering_instance_list()
    assert result["totalRows"] == 0
    assert result["vpcPeeringInstanceList"] == []


@pytest.mark.asyncio
async def test_aget_vpc_peering_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_VPC_PEERING_RESPONSE)
    result = await make_api().aget_vpc_peering_instance_list()
    assert isinstance(result, dict)
    assert result["vpcPeeringInstanceList"][0]["vpcPeeringName"] == "my-peering"
