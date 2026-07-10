from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

CDSS_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://clouddatastreamingservice.apigw.ntruss.com",
    NcpEnv.GOV: "https://clouddatastreamingservice.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://clouddatastreamingservice.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class CdssApi(NcpHttpAdapter):
    """Cloud Data Streaming Service (vcdss). Sig-v2, REST + JSON."""

    path_prefix: ClassVar[str] = "/api/v1"

    # --- Cluster ---

    def get_cluster_list(self) -> dict[str, Any]:
        return self.request("GET", "/cluster")

    async def aget_cluster_list(self) -> dict[str, Any]:
        return await self.arequest("GET", "/cluster")

    def get_cluster(self, service_group_instance_no: str) -> dict[str, Any]:
        return self.request("GET", f"/cluster/{service_group_instance_no}")

    async def aget_cluster(self, service_group_instance_no: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/cluster/{service_group_instance_no}")

    def create_cluster(self, body: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/cluster", json=body)

    async def acreate_cluster(self, body: dict[str, Any]) -> dict[str, Any]:
        return await self.arequest("POST", "/cluster", json=body)

    def delete_cluster(self, service_group_instance_no: str) -> dict[str, Any]:
        return self.request("DELETE", f"/cluster/{service_group_instance_no}")

    async def adelete_cluster(self, service_group_instance_no: str) -> dict[str, Any]:
        return await self.arequest("DELETE", f"/cluster/{service_group_instance_no}")

    def change_cluster_broker_count(
        self, service_group_instance_no: str, *, broker_node_count: int
    ) -> dict[str, Any]:
        body = {"brokerNodeCount": broker_node_count}
        return self.request(
            "PATCH", f"/cluster/{service_group_instance_no}/brokerNodeCount", json=body
        )

    async def achange_cluster_broker_count(
        self, service_group_instance_no: str, *, broker_node_count: int
    ) -> dict[str, Any]:
        body = {"brokerNodeCount": broker_node_count}
        return await self.arequest(
            "PATCH", f"/cluster/{service_group_instance_no}/brokerNodeCount", json=body
        )

    def get_cluster_metrics(
        self,
        service_group_instance_no: str,
        *,
        metric_name_list: list[str] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        period: str | None = None,
        interval: str | None = None,
        aggregate: str | None = None,
    ) -> dict[str, Any]:
        body = _body(
            metricNameList=metric_name_list,
            startTime=start_time,
            endTime=end_time,
            period=period,
            interval=interval,
            aggregate=aggregate,
        )
        return self.request(
            "GET",
            f"/cluster/{service_group_instance_no}/metrics",
            json=body if body else None,
        )

    async def aget_cluster_metrics(
        self,
        service_group_instance_no: str,
        *,
        metric_name_list: list[str] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        period: str | None = None,
        interval: str | None = None,
        aggregate: str | None = None,
    ) -> dict[str, Any]:
        body = _body(
            metricNameList=metric_name_list,
            startTime=start_time,
            endTime=end_time,
            period=period,
            interval=interval,
            aggregate=aggregate,
        )
        return await self.arequest(
            "GET",
            f"/cluster/{service_group_instance_no}/metrics",
            json=body if body else None,
        )

    def get_cluster_broker_metrics(
        self,
        service_group_instance_no: str,
        broker_no: str,
        *,
        metric_name_list: list[str] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> dict[str, Any]:
        body = _body(
            metricNameList=metric_name_list, startTime=start_time, endTime=end_time
        )
        return self.request(
            "GET",
            f"/cluster/{service_group_instance_no}/broker/{broker_no}/metrics",
            json=body if body else None,
        )

    async def aget_cluster_broker_metrics(
        self,
        service_group_instance_no: str,
        broker_no: str,
        *,
        metric_name_list: list[str] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> dict[str, Any]:
        body = _body(
            metricNameList=metric_name_list, startTime=start_time, endTime=end_time
        )
        return await self.arequest(
            "GET",
            f"/cluster/{service_group_instance_no}/broker/{broker_no}/metrics",
            json=body if body else None,
        )

    # --- Config Groups ---

    def get_config_group_list(
        self, *, kafka_version_id: str | None = None
    ) -> dict[str, Any]:
        params = _body(kafkaVersionId=kafka_version_id)
        return self.request("GET", "/configGroup", params=params if params else None)

    async def aget_config_group_list(
        self, *, kafka_version_id: str | None = None
    ) -> dict[str, Any]:
        params = _body(kafkaVersionId=kafka_version_id)
        return await self.arequest(
            "GET", "/configGroup", params=params if params else None
        )

    def get_config_group(self, config_group_no: str) -> dict[str, Any]:
        return self.request("GET", f"/configGroup/{config_group_no}")

    async def aget_config_group(self, config_group_no: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/configGroup/{config_group_no}")

    def create_config_group(self, body: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/configGroup", json=body)

    async def acreate_config_group(self, body: dict[str, Any]) -> dict[str, Any]:
        return await self.arequest("POST", "/configGroup", json=body)

    def change_config_group(
        self, config_group_no: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return self.request("PATCH", f"/configGroup/{config_group_no}", json=body)

    async def achange_config_group(
        self, config_group_no: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.arequest(
            "PATCH", f"/configGroup/{config_group_no}", json=body
        )

    def delete_config_group(self, config_group_no: str) -> dict[str, Any]:
        return self.request("DELETE", f"/configGroup/{config_group_no}")

    async def adelete_config_group(self, config_group_no: str) -> dict[str, Any]:
        return await self.arequest("DELETE", f"/configGroup/{config_group_no}")

    # --- Metadata (product lists, kafka versions) ---

    def get_kafka_version_list(self) -> dict[str, Any]:
        return self.request("GET", "/kafkaVersion")

    async def aget_kafka_version_list(self) -> dict[str, Any]:
        return await self.arequest("GET", "/kafkaVersion")

    def get_node_product_list(
        self, *, kafka_version_id: str | None = None
    ) -> dict[str, Any]:
        params = _body(kafkaVersionId=kafka_version_id)
        return self.request("GET", "/nodeProduct", params=params if params else None)

    async def aget_node_product_list(
        self, *, kafka_version_id: str | None = None
    ) -> dict[str, Any]:
        params = _body(kafkaVersionId=kafka_version_id)
        return await self.arequest(
            "GET", "/nodeProduct", params=params if params else None
        )

    def get_cloud_log_analytics_list(self) -> dict[str, Any]:
        return self.request("GET", "/cloudLogAnalytics")

    async def aget_cloud_log_analytics_list(self) -> dict[str, Any]:
        return await self.arequest("GET", "/cloudLogAnalytics")

    def get_object_storage_bucket_list(self) -> dict[str, Any]:
        return self.request("GET", "/objectStorage/bucket")

    async def aget_object_storage_bucket_list(self) -> dict[str, Any]:
        return await self.arequest("GET", "/objectStorage/bucket")

    def get_vpc_list(self) -> dict[str, Any]:
        return self.request("GET", "/vpc")

    async def aget_vpc_list(self) -> dict[str, Any]:
        return await self.arequest("GET", "/vpc")

    def get_subnet_list(self, *, vpc_no: str | None = None) -> dict[str, Any]:
        params = _body(vpcNo=vpc_no)
        return self.request("GET", "/subnet", params=params if params else None)

    async def aget_subnet_list(self, *, vpc_no: str | None = None) -> dict[str, Any]:
        params = _body(vpcNo=vpc_no)
        return await self.arequest("GET", "/subnet", params=params if params else None)

    def get_login_key_list(self) -> dict[str, Any]:
        return self.request("GET", "/loginKey")

    async def aget_login_key_list(self) -> dict[str, Any]:
        return await self.arequest("GET", "/loginKey")
