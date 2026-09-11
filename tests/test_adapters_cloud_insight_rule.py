from __future__ import annotations

from typing import Any

from ncp_api.adapters.cloud_insight_rule import (
    CloudInsightRuleApi,
    MetricRuleItem,
    MonitorTargetItem,
    RecipientNotification,
    SuspendRuleItem,
)
from ncp_api.auth import HmacSigner

BASE_URL = "https://cw.apigw.ntruss.com"

METRIC_ITEM = MetricRuleItem(
    calculation="AVG",
    condition="GT",
    metric="avg_cpu_used_rto",
    threshold=90,
    duration=1,
    event_level="CRITICAL",
    dimensions=[{"dim": "type", "val": "svr"}],
)

MONITOR_ITEM = MonitorTargetItem(
    nrn="nrn:PUB:SERVER:KR:1234:server:1111", resource_id="1111", resource_name="web-01"
)

RECIPIENT = RecipientNotification(
    group_num=8168, notify_types=["SMS", "EMAIL"], enable_noti_when_event_close=False
)


def make_api() -> CloudInsightRuleApi:
    return CloudInsightRuleApi(BASE_URL, HmacSigner("testkey", "testsecret"))


# -- MetricsGrp ---------------------------------------------------------


def test_create_metrics_group_path_and_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "mg-1"})
    make_api().create_metrics_group(
        prod_key="prod-1",
        group_name="server-usage",
        group_desc="desc",
        metrics_group_items=[METRIC_ITEM],
    )
    sent = httpx_mock.get_requests()[0]
    assert "/cw_fea/real/cw/api/rule/group/metrics" in str(sent.url)
    import json

    body = json.loads(sent.content)
    assert body["prodKey"] == "prod-1"
    assert body["metricsGroupItems"][0]["eventLevel"] == "CRITICAL"
    assert body["metricsGroupItems"][0]["threshold"] == 90
    assert body["temporaryGroup"] is False


async def test_acreate_metrics_group_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "mg-1"})
    result = await make_api().acreate_metrics_group(
        prod_key="prod-1",
        group_name="server-usage",
        group_desc="desc",
        metrics_group_items=[METRIC_ITEM],
    )
    assert result == {"id": "mg-1"}


def test_get_metrics_group_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "mg-1"})
    make_api().get_metrics_group(prod_key="prod-1", metrics_group_id="mg-1")
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/metrics/query/prod-1/mg-1" in str(sent.url)


def test_get_metrics_group_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=[{"id": "mg-1"}])
    result = make_api().get_metrics_group_list(prod_key="prod-1")
    assert result == [{"id": "mg-1"}]
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/metrics/query/prod-1" in str(sent.url)


def test_update_metrics_group_path_and_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "mg-1"})
    make_api().update_metrics_group(
        metrics_group_id="mg-1",
        group_name="server-usage-2",
        group_desc="desc2",
        metrics_group_items=[METRIC_ITEM],
    )
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/metrics/update" in str(sent.url)
    import json

    body = json.loads(sent.content)
    assert body["id"] == "mg-1"


def test_delete_metrics_group_path_and_query(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={})
    make_api().delete_metrics_group(
        prod_key="prod-1", metrics_group_ids=["mg-1", "mg-2"]
    )
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/metrics/del" in str(sent.url)
    assert "prodKey=prod-1" in str(sent.url)


def test_delete_metrics_group_by_prod_key_and_id_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={})
    make_api().delete_metrics_group_by_prod_key_and_id(
        prod_key="prod-1", metrics_group_id="mg-1"
    )
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/metrics/del/prod-1/mg-1" in str(sent.url)


def test_delete_metrics_group_force_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={})
    make_api().delete_metrics_group_force(prod_key="prod-1", metrics_group_ids=["mg-1"])
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/metric/groups" in str(sent.url)
    assert "prodKey=prod-1" in str(sent.url)


# -- MonitorGrp -----------------------------------------------------------


def test_create_monitor_group_path_and_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "mon-1"})
    make_api().create_monitor_group(
        prod_key="prod-1",
        group_name="targets",
        group_desc="desc",
        monitor_group_item_list=[MONITOR_ITEM],
    )
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/monitor" in str(sent.url)
    import json

    body = json.loads(sent.content)
    assert body["monitorGroupItemList"][0]["nrn"] == MONITOR_ITEM.nrn
    assert body["monitorGroupItemList"][0]["resourceId"] == "1111"


async def test_acreate_monitor_group_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "mon-1"})
    result = await make_api().acreate_monitor_group(
        prod_key="prod-1",
        group_name="targets",
        group_desc="desc",
        monitor_group_item_list=[MONITOR_ITEM],
    )
    assert result == {"id": "mon-1"}


def test_get_monitor_group_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "mon-1"})
    make_api().get_monitor_group(prod_key="prod-1", monitor_group_id="mon-1")
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/monitor/prod-1/mon-1" in str(sent.url)


def test_update_monitor_group_path_and_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "mon-1"})
    make_api().update_monitor_group(
        monitor_group_id="mon-1",
        group_name="targets-2",
        group_desc="desc2",
        monitor_group_item_list=[MONITOR_ITEM],
        prod_key="prod-1",
        prod_name="Server(VPC)",
    )
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "PUT"
    assert "/rule/group/monitor" in str(sent.url)


def test_delete_monitor_group_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={})
    make_api().delete_monitor_group(prod_key="prod-1", monitor_group_ids=["mon-1"])
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/monitor" in str(sent.url)
    assert "prodKey=prod-1" in str(sent.url)


def test_delete_monitor_group_force_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={})
    make_api().delete_monitor_group_force(
        prod_key="prod-1", monitor_group_ids=["mon-1"]
    )
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/monitor/groups" in str(sent.url)


def test_remove_resource_from_rules_path_and_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={})
    make_api().remove_resource_from_rules(
        prod_key="prod-1", resource_id="1111", rule_group_ids=["rg-1"]
    )
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/monitor/removeResourceFromRules" in str(sent.url)
    import json

    body = json.loads(sent.content)
    assert body["resourceId"] == "1111"
    assert body["ruleGroupIds"] == ["rg-1"]


# -- RuleGroup --------------------------------------------------------------


def test_create_rule_group_path_and_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "rg-1"})
    make_api().create_rule_group(
        prod_key="prod-1",
        group_name="server-rule",
        group_desc="desc",
        monitor_group_key=["mon-1"],
        metrics_group_key=["mg-1"],
        recipient_notifications=[RECIPIENT],
    )
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/ruleGrp" in str(sent.url)
    import json

    body = json.loads(sent.content)
    assert body["monitorGroupKey"] == ["mon-1"]
    assert body["metricsGroupKey"] == ["mg-1"]
    assert body["recipientNotifications"][0]["groupNum"] == 8168
    assert body["recipientNotifications"][0]["notifyTypes"] == ["SMS", "EMAIL"]


def test_create_rule_group_without_notification_omits_field(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "rg-1"})
    make_api().create_rule_group(
        prod_key="prod-1",
        group_name="server-rule",
        group_desc="desc",
        monitor_group_key=["mon-1"],
        metrics_group_key=["mg-1"],
    )
    sent = httpx_mock.get_requests()[0]
    import json

    body = json.loads(sent.content)
    assert "recipientNotifications" not in body


async def test_acreate_rule_group_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "rg-1"})
    result = await make_api().acreate_rule_group(
        prod_key="prod-1",
        group_name="server-rule",
        group_desc="desc",
        monitor_group_key=["mon-1"],
        metrics_group_key=["mg-1"],
    )
    assert result == {"id": "rg-1"}


def test_get_rule_group_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "rg-1"})
    make_api().get_rule_group(prod_key="prod-1", rule_group_id="rg-1")
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/ruleGrp/query/prod-1/rg-1" in str(sent.url)


def test_get_rule_group_list_path_and_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"items": []})
    make_api().get_rule_group_list(
        prod_key="prod-1", page_size=3, page_num=1, search=""
    )
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/ruleGrp/query" in str(sent.url)
    import json

    body = json.loads(sent.content)
    assert body["pageSize"] == 3
    assert body["pageNum"] == 1


def test_get_rule_group_by_metric_group_ids(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=[{"id": "rg-1"}])
    result = make_api().get_rule_group_by_metric_group_ids(
        prod_key="prod-1", metric_group_ids=["mg-1"]
    )
    assert result == [{"id": "rg-1"}]
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/metric/group/related" in str(sent.url)
    assert "prodKey=prod-1" in str(sent.url)


def test_get_rule_group_by_monitor_group_ids(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=[{"id": "rg-1"}])
    result = make_api().get_rule_group_by_monitor_group_ids(
        prod_key="prod-1", monitor_group_ids=["mon-1"]
    )
    assert result == [{"id": "rg-1"}]
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/monitor/group/related" in str(sent.url)


def test_update_rule_group_path_and_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "rg-1"})
    make_api().update_rule_group(
        rule_group_id="rg-1",
        prod_key="prod-1",
        group_name="server-rule-2",
        group_desc="desc2",
        monitor_group_key=["mon-1"],
        metrics_group_key=["mg-1"],
        recipient_notifications=[RECIPIENT],
        suspend_rule_items=[
            SuspendRuleItem(resource_id="1111", metric_group_item_id="mgi-1")
        ],
    )
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/ruleGrp/update" in str(sent.url)
    import json

    body = json.loads(sent.content)
    assert body["id"] == "rg-1"
    assert body["suspendRuleItems"][0]["metricGroupItemId"] == "mgi-1"


def test_delete_rule_group_path_and_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={})
    make_api().delete_rule_group(prod_key="prod-1", rule_group_id="rg-1")
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/ruleGrp/del" in str(sent.url)
    import json

    body = json.loads(sent.content)
    assert body["items"] == [{"prodKey": "prod-1", "ruleGroupId": "rg-1"}]


def test_copy_rule_group_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "rg-2"})
    make_api().copy_rule_group(rule_group_id="rg-1")
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "PUT"
    assert "/rule/group/ruleGrp/copy/rg-1" in str(sent.url)


def test_create_rule_directly_path_and_body(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "rg-1"})
    make_api().create_rule_directly(
        prod_key="prod-1",
        group_name="direct-rule",
        group_desc="desc",
        metrics_group_name="mg-name",
        metrics_group_desc="mg-desc",
        metrics_group_items=[METRIC_ITEM],
        monitor_group_name="mon-name",
        monitor_group_desc="mon-desc",
        monitor_group_item_list=[MONITOR_ITEM],
    )
    sent = httpx_mock.get_requests()[0]
    assert "/rule/group/ruleGrp/createDirectly" in str(sent.url)
    import json

    body = json.loads(sent.content)
    assert body["metricsGroup"]["groupName"] == "mg-name"
    assert body["monitorGroup"]["groupName"] == "mon-name"


# -- Notification recipients -------------------------------------------------


def test_get_notification_recipient_list_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=[{"groupNum": 8168, "groupName": "test-nr"}])
    result = make_api().get_notification_recipient_list()
    assert result == [{"groupNum": 8168, "groupName": "test-nr"}]
    sent = httpx_mock.get_requests()[0]
    assert "/rule/notify/groups" in str(sent.url)


async def test_aget_notification_recipient_list_returns_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=[{"groupNum": 8168}])
    result = await make_api().aget_notification_recipient_list()
    assert result == [{"groupNum": 8168}]


def test_create_metrics_group_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"id": "mg-1"})
    make_api().create_metrics_group(
        prod_key="prod-1",
        group_name="server-usage",
        group_desc="desc",
        metrics_group_items=[METRIC_ITEM],
    )
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers
