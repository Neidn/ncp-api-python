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
    make_api().get_load_balancer_instance_list(
        load_balancer_instance_no_list=["123456", "789012"]
    )
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
    make_api().get_load_balancer_instance_list(
        sorted_by="loadBalancerName", sorting_order="ASC"
    )
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


# --- get_load_balancer_listener_list ---

SAMPLE_LISTENER_RESPONSE = {
    "getLoadBalancerListenerListResponse": {
        "requestId": "req-listener-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "loadBalancerListenerList": [
            {
                "loadBalancerInstanceNo": "11111",
                "loadBalancerListenerNo": "22222",
                "protocolType": {"code": "HTTP", "codeName": "HTTP protocol"},
                "port": 80,
                "useHttp2": False,
            }
        ],
    }
}


def test_get_load_balancer_listener_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_LISTENER_RESPONSE)
    result = make_api().get_load_balancer_listener_list(
        load_balancer_instance_no="11111"
    )
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
    assert result["loadBalancerListenerList"][0]["port"] == 80


def test_get_load_balancer_listener_list_correct_path_and_params(
    httpx_mock: Any,
) -> None:
    httpx_mock.add_response(json=SAMPLE_LISTENER_RESPONSE)
    make_api().get_load_balancer_listener_list(load_balancer_instance_no="11111")
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "/vloadbalancer/v2/getLoadBalancerListenerList" in url
    assert "loadBalancerInstanceNo=11111" in url


def test_get_load_balancer_listener_list_region_code(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_LISTENER_RESPONSE)
    make_api().get_load_balancer_listener_list(
        load_balancer_instance_no="11111", region_code="KR"
    )
    url = str(httpx_mock.get_requests()[0].url)
    assert "regionCode=KR" in url


async def test_aget_load_balancer_listener_list_returns_dict(
    httpx_mock: Any,
) -> None:
    httpx_mock.add_response(json=SAMPLE_LISTENER_RESPONSE)
    result = await make_api().aget_load_balancer_listener_list(
        load_balancer_instance_no="11111"
    )
    assert isinstance(result, dict)
    assert result["loadBalancerListenerList"][0]["loadBalancerListenerNo"] == "22222"


# --- get_load_balancer_rule_list ---

SAMPLE_RULE_RESPONSE = {
    "getLoadBalancerRuleListResponse": {
        "requestId": "req-rule-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "loadBalancerRuleList": [
            {
                "loadBalancerListenerNo": "22222",
                "loadBalancerRuleNo": "33333",
                "priority": 10000,
                "loadBalancerRuleConditionList": [
                    {"ruleConditionType": {"code": "DEFAULT"}}
                ],
            }
        ],
    }
}


def test_get_load_balancer_rule_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RULE_RESPONSE)
    result = make_api().get_load_balancer_rule_list(load_balancer_listener_no="22222")
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
    assert result["loadBalancerRuleList"][0]["loadBalancerRuleNo"] == "33333"


def test_get_load_balancer_rule_list_correct_path_and_params(
    httpx_mock: Any,
) -> None:
    httpx_mock.add_response(json=SAMPLE_RULE_RESPONSE)
    make_api().get_load_balancer_rule_list(load_balancer_listener_no="22222")
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "/vloadbalancer/v2/getLoadBalancerRuleList" in url
    assert "loadBalancerListenerNo=22222" in url


def test_get_load_balancer_rule_list_region_code(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RULE_RESPONSE)
    make_api().get_load_balancer_rule_list(
        load_balancer_listener_no="22222", region_code="KR"
    )
    url = str(httpx_mock.get_requests()[0].url)
    assert "regionCode=KR" in url


async def test_aget_load_balancer_rule_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RULE_RESPONSE)
    result = await make_api().aget_load_balancer_rule_list(
        load_balancer_listener_no="22222"
    )
    assert isinstance(result, dict)
    assert result["loadBalancerRuleList"][0]["priority"] == 10000


# --- get_target_list ---

SAMPLE_TARGET_RESPONSE = {
    "getTargetListResponse": {
        "requestId": "req-target-001",
        "returnCode": "0",
        "returnMessage": "success",
        "totalRows": 1,
        "targetList": [
            {
                "targetNo": "44444",
                "targetName": "my-target",
                "targetIp": "10.0.0.1",
                "healthCheckStatus": {"code": "UP", "codeName": "Health UP state"},
            }
        ],
    }
}


def test_get_target_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_TARGET_RESPONSE)
    result = make_api().get_target_list(target_group_no="55555")
    assert isinstance(result, dict)
    assert result["totalRows"] == 1
    assert result["targetList"][0]["targetNo"] == "44444"


def test_get_target_list_correct_path_and_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_TARGET_RESPONSE)
    make_api().get_target_list(target_group_no="55555")
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "/vloadbalancer/v2/getTargetList" in url
    assert "targetGroupNo=55555" in url


def test_get_target_list_region_code(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_TARGET_RESPONSE)
    make_api().get_target_list(target_group_no="55555", region_code="KR")
    url = str(httpx_mock.get_requests()[0].url)
    assert "regionCode=KR" in url


async def test_aget_target_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_TARGET_RESPONSE)
    result = await make_api().aget_target_list(target_group_no="55555")
    assert isinstance(result, dict)
    assert result["targetList"][0]["healthCheckStatus"]["code"] == "UP"
