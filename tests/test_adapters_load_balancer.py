from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.load_balancer import LoadBalancerApi
from ncp_api.exceptions import NcpApiError, NcpAuthError

BASE_URL = "https://ncloud.apigw.ntruss.com"

SAMPLE_RESPONSE = {
    "getLoadBalancerInstanceListResponse": {
        "requestId": "req-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 2,
        "loadBalancerInstanceList": [
            {
                "loadBalancerInstanceNo": "123456",
                "loadBalancerName": "my-lb",
                "loadBalancerTypeCode": "NETWORK",
                "loadBalancerNetworkTypeCode": "PUBLIC",
                "loadBalancerStatusCode": "RUN",
                "vpcNo": "vpc-001",
            },
            {
                "loadBalancerInstanceNo": "789012",
                "loadBalancerName": "my-lb-2",
                "loadBalancerTypeCode": "APPLICATION",
                "loadBalancerNetworkTypeCode": "PRIVATE",
                "loadBalancerStatusCode": "RUN",
                "vpcNo": "vpc-001",
            },
        ],
    }
}

EMPTY_RESPONSE = {
    "getLoadBalancerInstanceListResponse": {
        "requestId": "req-002",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 0,
        "loadBalancerInstanceList": [],
    }
}

ERROR_RESPONSE = {
    "responseError": {
        "returnCode": "1300",
        "returnMessage": "Unauthenticated",
    }
}


def make_api() -> LoadBalancerApi:
    from ncp_api.auth import HmacSigner
    return LoadBalancerApi(BASE_URL, HmacSigner("testkey", "testsecret"))


def test_get_lb_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    result = make_api().get_load_balancer_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 2


def test_get_lb_list_instance_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    result = make_api().get_load_balancer_instance_list()
    lb_list = result["loadBalancerInstanceList"]
    assert len(lb_list) == 2
    assert lb_list[0]["loadBalancerName"] == "my-lb"
    assert lb_list[0]["loadBalancerTypeCode"] == "NETWORK"
    assert lb_list[1]["loadBalancerTypeCode"] == "APPLICATION"


def test_get_lb_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_load_balancer_instance_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
    assert "/vloadbalancer/v2/getLoadBalancerInstanceList" in str(sent.url)


def test_get_lb_list_region_code_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_load_balancer_instance_list(region_code="KR")
    sent = httpx_mock.get_requests()[0]
    assert "regionCode=KR" in str(sent.url)


def test_get_lb_list_name_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_load_balancer_instance_list(load_balancer_name="my-lb")
    sent = httpx_mock.get_requests()[0]
    assert "loadBalancerName=my-lb" in str(sent.url)


def test_get_lb_list_type_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_load_balancer_instance_list(load_balancer_type_code="NETWORK")
    sent = httpx_mock.get_requests()[0]
    assert "loadBalancerTypeCode=NETWORK" in str(sent.url)


def test_get_lb_list_network_type_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_load_balancer_instance_list(load_balancer_network_type_code="PUBLIC")
    sent = httpx_mock.get_requests()[0]
    assert "loadBalancerNetworkTypeCode=PUBLIC" in str(sent.url)


def test_get_lb_list_status_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_load_balancer_instance_list(load_balancer_status_code="RUN")
    sent = httpx_mock.get_requests()[0]
    assert "loadBalancerStatusCode=RUN" in str(sent.url)


def test_get_lb_list_vpc_no_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_load_balancer_instance_list(vpc_no="vpc-001")
    sent = httpx_mock.get_requests()[0]
    assert "vpcNo=vpc-001" in str(sent.url)


def test_get_lb_list_instance_no_list_indexed(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_load_balancer_instance_list(load_balancer_instance_no_list=["123456", "789012"])
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "loadBalancerInstanceNoList.1=123456" in url
    assert "loadBalancerInstanceNoList.2=789012" in url


def test_get_lb_list_pagination_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_load_balancer_instance_list(page_no=2, page_size=10)
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "pageNo=2" in url
    assert "pageSize=10" in url


def test_get_lb_list_sorting_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_load_balancer_instance_list(sorted_by="loadBalancerName", sorting_order="ASC")
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "sortedBy=loadBalancerName" in url
    assert "sortingOrder=ASC" in url


def test_get_lb_list_empty(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=EMPTY_RESPONSE)
    result = make_api().get_load_balancer_instance_list()
    assert result["totalRows"] == 0
    assert result["loadBalancerInstanceList"] == []


def test_get_lb_list_401_raises_auth_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(status_code=401, json=ERROR_RESPONSE)
    with pytest.raises(NcpAuthError):
        make_api().get_load_balancer_instance_list()


def test_get_lb_list_500_raises_api_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(status_code=500, json={"error": "server error"})
    with pytest.raises(NcpApiError):
        make_api().get_load_balancer_instance_list()


async def test_aget_lb_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    result = await make_api().aget_load_balancer_instance_list()
    assert isinstance(result, dict)
    assert result["totalRows"] == 2
    assert len(result["loadBalancerInstanceList"]) == 2
