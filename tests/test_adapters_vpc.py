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
    make_api().get_nat_gateway_instance_list(
        nat_gateway_instance_no_list=["55555", "66666"]
    )
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
    make_api().get_nat_gateway_instance_list(
        sorted_by="natGatewayName", sorting_order="DESC"
    )
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
    make_api().get_vpc_peering_instance_list(
        vpc_peering_instance_no_list=["77777", "88888"]
    )
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
    make_api().get_vpc_peering_instance_list(
        sorted_by="vpcPeeringName", sorting_order="ASC"
    )
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


# --- get_route_table_list ---

SAMPLE_ROUTE_TABLE_RESPONSE = {
    "getRouteTableListResponse": {
        "requestId": "req-rt-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "routeTableList": [
            {
                "routeTableNo": "11111",
                "routeTableName": "my-rt",
                "routeTableStatusCode": "RUN",
                "routeTableTypeCode": "CUSTOM",
                "vpcNo": "12345",
                "supportedSubnetTypeCode": "PUBLIC",
            }
        ],
    }
}

EMPTY_ROUTE_TABLE_RESPONSE = {
    "getRouteTableListResponse": {
        "requestId": "req-rt-002",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 0,
        "routeTableList": [],
    }
}


def test_get_route_table_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_TABLE_RESPONSE)
    result = make_api().get_route_table_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 1


def test_get_route_table_list_data(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_TABLE_RESPONSE)
    result = make_api().get_route_table_list()
    rt = result["routeTableList"][0]
    assert rt["routeTableName"] == "my-rt"
    assert rt["routeTableTypeCode"] == "CUSTOM"


def test_get_route_table_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_TABLE_RESPONSE)
    make_api().get_route_table_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
    assert "/vpc/v2/getRouteTableList" in str(sent.url)


def test_get_route_table_list_name_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_TABLE_RESPONSE)
    make_api().get_route_table_list(route_table_name="my-rt")
    assert "routeTableName=my-rt" in str(httpx_mock.get_requests()[0].url)


def test_get_route_table_list_type_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_TABLE_RESPONSE)
    make_api().get_route_table_list(route_table_type_code="CUSTOM")
    assert "routeTableTypeCode=CUSTOM" in str(httpx_mock.get_requests()[0].url)


def test_get_route_table_list_vpc_no_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_TABLE_RESPONSE)
    make_api().get_route_table_list(vpc_no="12345")
    assert "vpcNo=12345" in str(httpx_mock.get_requests()[0].url)


def test_get_route_table_list_subnet_type_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_TABLE_RESPONSE)
    make_api().get_route_table_list(supported_subnet_type_code="PUBLIC")
    assert "supportedSubnetTypeCode=PUBLIC" in str(httpx_mock.get_requests()[0].url)


def test_get_route_table_list_no_list_indexed(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_TABLE_RESPONSE)
    make_api().get_route_table_list(route_table_no_list=["11111", "22222"])
    url = str(httpx_mock.get_requests()[0].url)
    assert "routeTableNoList.1=11111" in url
    assert "routeTableNoList.2=22222" in url


def test_get_route_table_list_empty(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=EMPTY_ROUTE_TABLE_RESPONSE)
    result = make_api().get_route_table_list()
    assert result["totalRows"] == 0
    assert result["routeTableList"] == []


@pytest.mark.asyncio
async def test_aget_route_table_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_TABLE_RESPONSE)
    result = await make_api().aget_route_table_list(vpc_no="12345")
    assert isinstance(result, dict)
    assert result["routeTableList"][0]["routeTableNo"] == "11111"


# --- get_route_table_subnet_list ---

SAMPLE_RT_SUBNET_RESPONSE = {
    "getRouteTableSubnetListResponse": {
        "requestId": "req-rts-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "routeTableSubnetList": [
            {
                "subnetNo": "99999",
                "subnetName": "my-subnet",
                "subnet": "10.0.1.0/24",
                "subnetTypeCode": "PUBLIC",
            }
        ],
    }
}


def test_get_route_table_subnet_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RT_SUBNET_RESPONSE)
    result = make_api().get_route_table_subnet_list("11111")
    assert isinstance(result, dict)
    assert result["totalRows"] == 1


def test_get_route_table_subnet_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RT_SUBNET_RESPONSE)
    make_api().get_route_table_subnet_list("11111")
    sent = httpx_mock.get_requests()[0]
    assert "/vpc/v2/getRouteTableSubnetList" in str(sent.url)
    assert "routeTableNo=11111" in str(sent.url)


def test_get_route_table_subnet_list_subnet_no_list_indexed(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RT_SUBNET_RESPONSE)
    make_api().get_route_table_subnet_list("11111", subnet_no_list=["99999", "88888"])
    url = str(httpx_mock.get_requests()[0].url)
    assert "subnetNoList.1=99999" in url
    assert "subnetNoList.2=88888" in url


def test_get_route_table_subnet_list_pagination_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RT_SUBNET_RESPONSE)
    make_api().get_route_table_subnet_list("11111", page_no=0, page_size=10)
    url = str(httpx_mock.get_requests()[0].url)
    assert "pageNo=0" in url
    assert "pageSize=10" in url


@pytest.mark.asyncio
async def test_aget_route_table_subnet_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RT_SUBNET_RESPONSE)
    result = await make_api().aget_route_table_subnet_list("11111")
    assert isinstance(result, dict)
    assert result["routeTableSubnetList"][0]["subnetName"] == "my-subnet"


# --- get_route_list ---

SAMPLE_ROUTE_RESPONSE = {
    "getRouteListResponse": {
        "requestId": "req-route-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 2,
        "routeList": [
            {
                "destinationCidrBlock": "0.0.0.0/0",
                "targetName": "INTERNET_GATEWAY",
                "targetNo": "igw-001",
                "routeTableNo": "11111",
            },
            {
                "destinationCidrBlock": "10.0.0.0/16",
                "targetName": "LOCAL",
                "targetNo": None,
                "routeTableNo": "11111",
            },
        ],
    }
}


def test_get_route_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_RESPONSE)
    result = make_api().get_route_list("11111")
    assert isinstance(result, dict)
    assert result["totalRows"] == 2


def test_get_route_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_RESPONSE)
    make_api().get_route_list("11111")
    sent = httpx_mock.get_requests()[0]
    assert "/vpc/v2/getRouteList" in str(sent.url)
    assert "routeTableNo=11111" in str(sent.url)


def test_get_route_list_data(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_RESPONSE)
    result = make_api().get_route_list("11111")
    routes = result["routeList"]
    assert routes[0]["destinationCidrBlock"] == "0.0.0.0/0"
    assert routes[1]["destinationCidrBlock"] == "10.0.0.0/16"


def test_get_route_list_cidr_filter(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_RESPONSE)
    make_api().get_route_list("11111", destination_cidr_block="0.0.0.0/0")
    url = str(httpx_mock.get_requests()[0].url)
    assert (
        "destinationCidrBlock=0.0.0.0%2F0" in url
        or "destinationCidrBlock=0.0.0.0/0" in url
    )


def test_get_route_list_pagination_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_RESPONSE)
    make_api().get_route_list("11111", page_no=1, page_size=50)
    url = str(httpx_mock.get_requests()[0].url)
    assert "pageNo=1" in url
    assert "pageSize=50" in url


@pytest.mark.asyncio
async def test_aget_route_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_ROUTE_RESPONSE)
    result = await make_api().aget_route_list("11111")
    assert isinstance(result, dict)
    assert len(result["routeList"]) == 2
