from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar, cast

from ncp_api.adapters.base import NcpHttpAdapter


@dataclass
class MetricRuleItem:
    """One metric threshold within a MetricsGrp (rule template), e.g. CPU>=90."""

    calculation: str  # AVG, MAX, MIN, SUM, COUNT
    condition: str  # GT, GTE, LT, LTE, EQ, NEQ
    metric: str
    threshold: float
    duration: int
    event_level: str  # INFO, WARNING, CRITICAL
    dimensions: list[dict[str, str]] = field(default_factory=list)


@dataclass
class MonitorTargetItem:
    """One monitored resource (Server, CDB instance, ...) within a MonitorGrp."""

    nrn: str
    resource_id: str
    resource_name: str | None = None


@dataclass
class RecipientNotification:
    """Notification recipient group attached to a RuleGroup."""

    group_num: int
    notify_types: list[str]  # SMS, EMAIL
    enable_noti_when_event_close: bool = False


@dataclass
class SuspendRuleItem:
    """A (resource, metric rule item) pair whose notification is suspended."""

    resource_id: str
    metric_group_item_id: str


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def _params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


def _metric_rule_item_dict(item: MetricRuleItem) -> dict[str, Any]:
    return {
        "calculation": item.calculation,
        "condition": item.condition,
        "metric": item.metric,
        "threshold": item.threshold,
        "duration": item.duration,
        "eventLevel": item.event_level,
        "dimensions": item.dimensions,
    }


def _monitor_target_item_dict(item: MonitorTargetItem) -> dict[str, Any]:
    return _body(
        nrn=item.nrn,
        resourceId=item.resource_id,
        resourceName=item.resource_name,
    )


def _recipient_notification_dict(item: RecipientNotification) -> dict[str, Any]:
    return {
        "groupNum": item.group_num,
        "notifyTypes": item.notify_types,
        "enableNotiWhenEventClose": item.enable_noti_when_event_close,
    }


def _suspend_rule_item_dict(item: SuspendRuleItem) -> dict[str, Any]:
    return {
        "resourceId": item.resource_id,
        "metricGroupItemId": item.metric_group_item_id,
    }


class CloudInsightRuleApi(NcpHttpAdapter):
    """Cloud Insight Event Rule (MetricsGrp/MonitorGrp/RuleGroup). Sig-v2, REST+JSON.

    Event Rule = MetricsGrp (rule template: metric + threshold, e.g. CPU>=90)
    bound to a MonitorGrp (target group: Server/CDB resources) via RuleGroup, with
    optional RecipientNotification groups for alerting.
    """

    path_prefix: ClassVar[str] = "/cw_fea/real/cw/api"

    # -- MetricsGrp (rule template) --------------------------------------

    def create_metrics_group(
        self,
        *,
        prod_key: str,
        group_name: str,
        group_desc: str,
        metrics_group_items: list[MetricRuleItem],
        temporary_group: bool = False,
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key,
            groupName=group_name,
            groupDesc=group_desc,
            metricsGroupItems=[_metric_rule_item_dict(i) for i in metrics_group_items],
            temporaryGroup=temporary_group,
        )
        return self.request("POST", "/rule/group/metrics", json=body)

    async def acreate_metrics_group(
        self,
        *,
        prod_key: str,
        group_name: str,
        group_desc: str,
        metrics_group_items: list[MetricRuleItem],
        temporary_group: bool = False,
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key,
            groupName=group_name,
            groupDesc=group_desc,
            metricsGroupItems=[_metric_rule_item_dict(i) for i in metrics_group_items],
            temporaryGroup=temporary_group,
        )
        return await self.arequest("POST", "/rule/group/metrics", json=body)

    def get_metrics_group(
        self, *, prod_key: str, metrics_group_id: str
    ) -> dict[str, Any]:
        return self.request(
            "GET", f"/rule/group/metrics/query/{prod_key}/{metrics_group_id}"
        )

    async def aget_metrics_group(
        self, *, prod_key: str, metrics_group_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/rule/group/metrics/query/{prod_key}/{metrics_group_id}"
        )

    def get_metrics_group_list(self, *, prod_key: str) -> list[dict[str, Any]]:
        raw = self.request("GET", f"/rule/group/metrics/query/{prod_key}")
        return cast(list[dict[str, Any]], raw)

    async def aget_metrics_group_list(self, *, prod_key: str) -> list[dict[str, Any]]:
        raw = await self.arequest("GET", f"/rule/group/metrics/query/{prod_key}")
        return cast(list[dict[str, Any]], raw)

    def update_metrics_group(
        self,
        *,
        metrics_group_id: str,
        group_name: str,
        group_desc: str,
        metrics_group_items: list[MetricRuleItem],
    ) -> dict[str, Any]:
        body = _body(
            id=metrics_group_id,
            groupName=group_name,
            groupDesc=group_desc,
            metricsGroupItems=[_metric_rule_item_dict(i) for i in metrics_group_items],
        )
        return self.request("POST", "/rule/group/metrics/update", json=body)

    async def aupdate_metrics_group(
        self,
        *,
        metrics_group_id: str,
        group_name: str,
        group_desc: str,
        metrics_group_items: list[MetricRuleItem],
    ) -> dict[str, Any]:
        body = _body(
            id=metrics_group_id,
            groupName=group_name,
            groupDesc=group_desc,
            metricsGroupItems=[_metric_rule_item_dict(i) for i in metrics_group_items],
        )
        return await self.arequest("POST", "/rule/group/metrics/update", json=body)

    def delete_metrics_group(
        self, *, prod_key: str, metrics_group_ids: list[str]
    ) -> dict[str, Any]:
        params = _params(prodKey=prod_key)
        return self.request(
            "DELETE", "/rule/group/metrics/del", params=params, json=metrics_group_ids
        )

    async def adelete_metrics_group(
        self, *, prod_key: str, metrics_group_ids: list[str]
    ) -> dict[str, Any]:
        params = _params(prodKey=prod_key)
        return await self.arequest(
            "DELETE", "/rule/group/metrics/del", params=params, json=metrics_group_ids
        )

    def delete_metrics_group_by_prod_key_and_id(
        self, *, prod_key: str, metrics_group_id: str
    ) -> dict[str, Any]:
        return self.request(
            "DELETE", f"/rule/group/metrics/del/{prod_key}/{metrics_group_id}"
        )

    async def adelete_metrics_group_by_prod_key_and_id(
        self, *, prod_key: str, metrics_group_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "DELETE", f"/rule/group/metrics/del/{prod_key}/{metrics_group_id}"
        )

    def delete_metrics_group_force(
        self, *, prod_key: str, metrics_group_ids: list[str]
    ) -> dict[str, Any]:
        params = _params(prodKey=prod_key)
        return self.request(
            "DELETE",
            "/rule/group/metric/groups",
            params=params,
            json=[{"id": i} for i in metrics_group_ids],
        )

    async def adelete_metrics_group_force(
        self, *, prod_key: str, metrics_group_ids: list[str]
    ) -> dict[str, Any]:
        params = _params(prodKey=prod_key)
        return await self.arequest(
            "DELETE",
            "/rule/group/metric/groups",
            params=params,
            json=[{"id": i} for i in metrics_group_ids],
        )

    # -- MonitorGrp (target group) ----------------------------------------

    def create_monitor_group(
        self,
        *,
        prod_key: str,
        group_name: str,
        group_desc: str,
        monitor_group_item_list: list[MonitorTargetItem],
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key,
            groupName=group_name,
            groupDesc=group_desc,
            monitorGroupItemList=[
                _monitor_target_item_dict(i) for i in monitor_group_item_list
            ],
        )
        return self.request("POST", "/rule/group/monitor", json=body)

    async def acreate_monitor_group(
        self,
        *,
        prod_key: str,
        group_name: str,
        group_desc: str,
        monitor_group_item_list: list[MonitorTargetItem],
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key,
            groupName=group_name,
            groupDesc=group_desc,
            monitorGroupItemList=[
                _monitor_target_item_dict(i) for i in monitor_group_item_list
            ],
        )
        return await self.arequest("POST", "/rule/group/monitor", json=body)

    def get_monitor_group(
        self, *, prod_key: str, monitor_group_id: str
    ) -> dict[str, Any]:
        return self.request("GET", f"/rule/group/monitor/{prod_key}/{monitor_group_id}")

    async def aget_monitor_group(
        self, *, prod_key: str, monitor_group_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/rule/group/monitor/{prod_key}/{monitor_group_id}"
        )

    def update_monitor_group(
        self,
        *,
        monitor_group_id: str,
        group_name: str,
        group_desc: str,
        monitor_group_item_list: list[MonitorTargetItem],
        prod_key: str,
        prod_name: str,
        temporary_group: bool = False,
        type_: str = "NORMAL",
    ) -> dict[str, Any]:
        body = _body(
            id=monitor_group_id,
            groupName=group_name,
            groupDesc=group_desc,
            monitorGroupItemList=[
                _monitor_target_item_dict(i) for i in monitor_group_item_list
            ],
            prodKey=prod_key,
            prodName=prod_name,
            temporaryGroup=temporary_group,
            type=type_,
        )
        return self.request("PUT", "/rule/group/monitor", json=body)

    async def aupdate_monitor_group(
        self,
        *,
        monitor_group_id: str,
        group_name: str,
        group_desc: str,
        monitor_group_item_list: list[MonitorTargetItem],
        prod_key: str,
        prod_name: str,
        temporary_group: bool = False,
        type_: str = "NORMAL",
    ) -> dict[str, Any]:
        body = _body(
            id=monitor_group_id,
            groupName=group_name,
            groupDesc=group_desc,
            monitorGroupItemList=[
                _monitor_target_item_dict(i) for i in monitor_group_item_list
            ],
            prodKey=prod_key,
            prodName=prod_name,
            temporaryGroup=temporary_group,
            type=type_,
        )
        return await self.arequest("PUT", "/rule/group/monitor", json=body)

    def delete_monitor_group(
        self, *, prod_key: str, monitor_group_ids: list[str]
    ) -> dict[str, Any]:
        params = _params(prodKey=prod_key)
        return self.request(
            "DELETE", "/rule/group/monitor", params=params, json=monitor_group_ids
        )

    async def adelete_monitor_group(
        self, *, prod_key: str, monitor_group_ids: list[str]
    ) -> dict[str, Any]:
        params = _params(prodKey=prod_key)
        return await self.arequest(
            "DELETE", "/rule/group/monitor", params=params, json=monitor_group_ids
        )

    def delete_monitor_group_force(
        self, *, prod_key: str, monitor_group_ids: list[str]
    ) -> dict[str, Any]:
        params = _params(prodKey=prod_key)
        return self.request(
            "DELETE",
            "/rule/group/monitor/groups",
            params=params,
            json=[{"id": i} for i in monitor_group_ids],
        )

    async def adelete_monitor_group_force(
        self, *, prod_key: str, monitor_group_ids: list[str]
    ) -> dict[str, Any]:
        params = _params(prodKey=prod_key)
        return await self.arequest(
            "DELETE",
            "/rule/group/monitor/groups",
            params=params,
            json=[{"id": i} for i in monitor_group_ids],
        )

    def remove_resource_from_rules(
        self, *, prod_key: str, resource_id: str, rule_group_ids: list[str]
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key, resourceId=resource_id, ruleGroupIds=rule_group_ids
        )
        return self.request(
            "POST", "/rule/group/monitor/removeResourceFromRules", json=body
        )

    async def aremove_resource_from_rules(
        self, *, prod_key: str, resource_id: str, rule_group_ids: list[str]
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key, resourceId=resource_id, ruleGroupIds=rule_group_ids
        )
        return await self.arequest(
            "POST", "/rule/group/monitor/removeResourceFromRules", json=body
        )

    # -- RuleGroup (event rule) -------------------------------------------

    def create_rule_group(
        self,
        *,
        prod_key: str,
        group_name: str,
        group_desc: str,
        monitor_group_key: list[str],
        metrics_group_key: list[str],
        recipient_notifications: list[RecipientNotification] | None = None,
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key,
            groupName=group_name,
            groupDesc=group_desc,
            monitorGroupKey=monitor_group_key,
            metricsGroupKey=metrics_group_key,
            recipientNotifications=(
                [_recipient_notification_dict(r) for r in recipient_notifications]
                if recipient_notifications is not None
                else None
            ),
        )
        return self.request("POST", "/rule/group/ruleGrp", json=body)

    async def acreate_rule_group(
        self,
        *,
        prod_key: str,
        group_name: str,
        group_desc: str,
        monitor_group_key: list[str],
        metrics_group_key: list[str],
        recipient_notifications: list[RecipientNotification] | None = None,
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key,
            groupName=group_name,
            groupDesc=group_desc,
            monitorGroupKey=monitor_group_key,
            metricsGroupKey=metrics_group_key,
            recipientNotifications=(
                [_recipient_notification_dict(r) for r in recipient_notifications]
                if recipient_notifications is not None
                else None
            ),
        )
        return await self.arequest("POST", "/rule/group/ruleGrp", json=body)

    def get_rule_group(self, *, prod_key: str, rule_group_id: str) -> dict[str, Any]:
        return self.request(
            "GET", f"/rule/group/ruleGrp/query/{prod_key}/{rule_group_id}"
        )

    async def aget_rule_group(
        self, *, prod_key: str, rule_group_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/rule/group/ruleGrp/query/{prod_key}/{rule_group_id}"
        )

    def get_rule_group_list(
        self,
        *,
        prod_key: str,
        page_size: int | None = None,
        page_num: int | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key, pageSize=page_size, pageNum=page_num, search=search
        )
        return self.request("POST", "/rule/group/ruleGrp/query", json=body)

    async def aget_rule_group_list(
        self,
        *,
        prod_key: str,
        page_size: int | None = None,
        page_num: int | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key, pageSize=page_size, pageNum=page_num, search=search
        )
        return await self.arequest("POST", "/rule/group/ruleGrp/query", json=body)

    def get_rule_group_by_metric_group_ids(
        self, *, prod_key: str, metric_group_ids: list[str]
    ) -> list[dict[str, Any]]:
        params = _params(prodKey=prod_key)
        raw = self.request(
            "POST",
            "/rule/group/metric/group/related",
            params=params,
            json=metric_group_ids,
        )
        return cast(list[dict[str, Any]], raw)

    async def aget_rule_group_by_metric_group_ids(
        self, *, prod_key: str, metric_group_ids: list[str]
    ) -> list[dict[str, Any]]:
        params = _params(prodKey=prod_key)
        raw = await self.arequest(
            "POST",
            "/rule/group/metric/group/related",
            params=params,
            json=metric_group_ids,
        )
        return cast(list[dict[str, Any]], raw)

    def get_rule_group_by_monitor_group_ids(
        self, *, prod_key: str, monitor_group_ids: list[str]
    ) -> list[dict[str, Any]]:
        params = _params(prodKey=prod_key)
        raw = self.request(
            "POST",
            "/rule/group/monitor/group/related",
            params=params,
            json=monitor_group_ids,
        )
        return cast(list[dict[str, Any]], raw)

    async def aget_rule_group_by_monitor_group_ids(
        self, *, prod_key: str, monitor_group_ids: list[str]
    ) -> list[dict[str, Any]]:
        params = _params(prodKey=prod_key)
        raw = await self.arequest(
            "POST",
            "/rule/group/monitor/group/related",
            params=params,
            json=monitor_group_ids,
        )
        return cast(list[dict[str, Any]], raw)

    def update_rule_group(
        self,
        *,
        rule_group_id: str,
        prod_key: str,
        group_name: str,
        group_desc: str,
        monitor_group_key: list[str],
        metrics_group_key: list[str],
        recipient_notifications: list[RecipientNotification] | None = None,
        suspend_rule_items: list[SuspendRuleItem] | None = None,
    ) -> dict[str, Any]:
        body = _body(
            id=rule_group_id,
            prodKey=prod_key,
            groupName=group_name,
            groupDesc=group_desc,
            monitorGroupKey=monitor_group_key,
            metricsGroupKey=metrics_group_key,
            recipientNotifications=(
                [_recipient_notification_dict(r) for r in recipient_notifications]
                if recipient_notifications is not None
                else None
            ),
            suspendRuleItems=(
                [_suspend_rule_item_dict(s) for s in suspend_rule_items]
                if suspend_rule_items is not None
                else None
            ),
        )
        return self.request("POST", "/rule/group/ruleGrp/update", json=body)

    async def aupdate_rule_group(
        self,
        *,
        rule_group_id: str,
        prod_key: str,
        group_name: str,
        group_desc: str,
        monitor_group_key: list[str],
        metrics_group_key: list[str],
        recipient_notifications: list[RecipientNotification] | None = None,
        suspend_rule_items: list[SuspendRuleItem] | None = None,
    ) -> dict[str, Any]:
        body = _body(
            id=rule_group_id,
            prodKey=prod_key,
            groupName=group_name,
            groupDesc=group_desc,
            monitorGroupKey=monitor_group_key,
            metricsGroupKey=metrics_group_key,
            recipientNotifications=(
                [_recipient_notification_dict(r) for r in recipient_notifications]
                if recipient_notifications is not None
                else None
            ),
            suspendRuleItems=(
                [_suspend_rule_item_dict(s) for s in suspend_rule_items]
                if suspend_rule_items is not None
                else None
            ),
        )
        return await self.arequest("POST", "/rule/group/ruleGrp/update", json=body)

    def delete_rule_group(self, *, prod_key: str, rule_group_id: str) -> dict[str, Any]:
        body = {"items": [{"prodKey": prod_key, "ruleGroupId": rule_group_id}]}
        return self.request("POST", "/rule/group/ruleGrp/del", json=body)

    async def adelete_rule_group(
        self, *, prod_key: str, rule_group_id: str
    ) -> dict[str, Any]:
        body = {"items": [{"prodKey": prod_key, "ruleGroupId": rule_group_id}]}
        return await self.arequest("POST", "/rule/group/ruleGrp/del", json=body)

    def copy_rule_group(self, *, rule_group_id: str) -> dict[str, Any]:
        return self.request("PUT", f"/rule/group/ruleGrp/copy/{rule_group_id}")

    async def acopy_rule_group(self, *, rule_group_id: str) -> dict[str, Any]:
        return await self.arequest("PUT", f"/rule/group/ruleGrp/copy/{rule_group_id}")

    def create_rule_directly(
        self,
        *,
        prod_key: str,
        group_name: str,
        group_desc: str,
        metrics_group_name: str,
        metrics_group_desc: str,
        metrics_group_items: list[MetricRuleItem],
        monitor_group_name: str,
        monitor_group_desc: str,
        monitor_group_item_list: list[MonitorTargetItem],
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key,
            groupName=group_name,
            groupDesc=group_desc,
            metricsGroup=_body(
                groupName=metrics_group_name,
                groupDesc=metrics_group_desc,
                metricsGroupItems=[
                    _metric_rule_item_dict(i) for i in metrics_group_items
                ],
            ),
            monitorGroup=_body(
                groupName=monitor_group_name,
                groupDesc=monitor_group_desc,
                monitorGroupItemList=[
                    _monitor_target_item_dict(i) for i in monitor_group_item_list
                ],
            ),
        )
        return self.request("POST", "/rule/group/ruleGrp/createDirectly", json=body)

    async def acreate_rule_directly(
        self,
        *,
        prod_key: str,
        group_name: str,
        group_desc: str,
        metrics_group_name: str,
        metrics_group_desc: str,
        metrics_group_items: list[MetricRuleItem],
        monitor_group_name: str,
        monitor_group_desc: str,
        monitor_group_item_list: list[MonitorTargetItem],
    ) -> dict[str, Any]:
        body = _body(
            prodKey=prod_key,
            groupName=group_name,
            groupDesc=group_desc,
            metricsGroup=_body(
                groupName=metrics_group_name,
                groupDesc=metrics_group_desc,
                metricsGroupItems=[
                    _metric_rule_item_dict(i) for i in metrics_group_items
                ],
            ),
            monitorGroup=_body(
                groupName=monitor_group_name,
                groupDesc=monitor_group_desc,
                monitorGroupItemList=[
                    _monitor_target_item_dict(i) for i in monitor_group_item_list
                ],
            ),
        )
        return await self.arequest(
            "POST", "/rule/group/ruleGrp/createDirectly", json=body
        )

    # -- Notification recipients ------------------------------------------

    def get_notification_recipient_list(self) -> list[dict[str, Any]]:
        raw = self.request("GET", "/rule/notify/groups")
        return cast(list[dict[str, Any]], raw)

    async def aget_notification_recipient_list(self) -> list[dict[str, Any]]:
        raw = await self.arequest("GET", "/rule/notify/groups")
        return cast(list[dict[str, Any]], raw)
