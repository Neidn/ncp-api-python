from __future__ import annotations

from typing import Any

from ncp_api.adapters.vpc_search_engine import VpcSearchEngineApi
from ncp_api.auth import HmacSigner

BASE_URL = "https://vpcsearchengine.apigw.gov-ntruss.com"

CLUSTER_INFO_LIST_RESPONSE = {
    "code": 0,
    "message": "SUCCESS",
    "result": {
        "currentPage": 1,
        "isFirst": True,
        "isLast": True,
        "pageSize": 20,
        "totalCount": 1,
        "totalPage": 1,
        "allowedClusters": [
            {
                "clusterName": "cluster000",
                "clusterStatus": "running",
                "serviceGroupInstanceNo": "1037000",
            }
        ],
        "disallowedClusters": [],
    },
    "requestId": "bb3354b1-0000-0000-0000-5bee2500c24f",
}

CLUSTER_NODE_LIST_RESPONSE = {
    "code": 0,
    "message": "SUCCESS",
    "result": {
        "contractNo": 19146995,
        "serviceGroupInstanceNo": 1037000,
        "serviceGroupName": "cluster006",
        "statusCode": "CREAT",
        "computeList": [
            {
                "computeInstanceNo": 1037001,
                "nodeRoleCode": "M",
                "hostName": "cluster006-m-6tvf",
            }
        ],
    },
    "requestId": "bb3354b1-0000-0000-0000-5bee2500c24f",
}


def make_api() -> VpcSearchEngineApi:
    return VpcSearchEngineApi(BASE_URL, HmacSigner("testkey", "testsecret"))


def test_get_cluster_info_list_default_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_INFO_LIST_RESPONSE)
    result = make_api().get_cluster_info_list()
    sent = httpx_mock.get_requests()[0]
    assert "/api/v2/cluster/getClusterInfoList" in str(sent.url)
    assert result["allowedClusters"][0]["clusterName"] == "cluster000"


def test_get_cluster_info_list_south_region_and_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_INFO_LIST_RESPONSE)
    make_api().get_cluster_info_list(
        api_version="krs-v2",
        input_text="cluster",
        vpc_name="myvpc",
        page_no=1,
        page_size=20,
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "/api/krs-v2/cluster/getClusterInfoList" in url
    assert "inputText=cluster" in url
    assert "vpcName=myvpc" in url
    assert "pageNo=1" in url
    assert "pageSize=20" in url


async def test_aget_cluster_info_list_returns_result(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_INFO_LIST_RESPONSE)
    result = await make_api().aget_cluster_info_list()
    assert result["totalCount"] == 1


def test_get_cluster_node_list_default_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_NODE_LIST_RESPONSE)
    result = make_api().get_cluster_node_list(service_group_instance_no="1037000")
    sent = httpx_mock.get_requests()[0]
    assert "/api/v2/cluster/getClusterNodeList/1037000" in str(sent.url)
    assert result["computeList"][0]["nodeRoleCode"] == "M"


def test_get_cluster_node_list_south_region(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_NODE_LIST_RESPONSE)
    make_api().get_cluster_node_list(
        service_group_instance_no="1037000", api_version="krs-v2"
    )
    sent = httpx_mock.get_requests()[0]
    assert "/api/krs-v2/cluster/getClusterNodeList/1037000" in str(sent.url)


async def test_aget_cluster_node_list_returns_result(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_NODE_LIST_RESPONSE)
    result = await make_api().aget_cluster_node_list(
        service_group_instance_no="1037000"
    )
    assert result["serviceGroupName"] == "cluster006"


def test_get_cluster_info_list_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=CLUSTER_INFO_LIST_RESPONSE)
    make_api().get_cluster_info_list()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers
