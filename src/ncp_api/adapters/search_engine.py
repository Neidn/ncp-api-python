from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

SEARCH_ENGINE_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://cloudsearchengine.apigw.ntruss.com",
    NcpEnv.GOV: "https://cloudsearchengine.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://cloudsearchengine.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class SearchEngineApi(NcpHttpAdapter):
    """Cloud Search Engine Service (vses). Sig-v2, REST + JSON."""

    path_prefix: ClassVar[str] = "/api/v1"

    # --- Clusters ---

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

    def change_manager_node_count(
        self, service_group_instance_no: str, *, manager_node_count: int
    ) -> dict[str, Any]:
        body = {"managerNodeCount": manager_node_count}
        return self.request(
            "PATCH", f"/cluster/{service_group_instance_no}/managerNodeCount", json=body
        )

    async def achange_manager_node_count(
        self, service_group_instance_no: str, *, manager_node_count: int
    ) -> dict[str, Any]:
        body = {"managerNodeCount": manager_node_count}
        return await self.arequest(
            "PATCH", f"/cluster/{service_group_instance_no}/managerNodeCount", json=body
        )

    def change_data_node_count(
        self, service_group_instance_no: str, *, data_node_count: int
    ) -> dict[str, Any]:
        body = {"dataNodeCount": data_node_count}
        return self.request(
            "PATCH", f"/cluster/{service_group_instance_no}/dataNodeCount", json=body
        )

    async def achange_data_node_count(
        self, service_group_instance_no: str, *, data_node_count: int
    ) -> dict[str, Any]:
        body = {"dataNodeCount": data_node_count}
        return await self.arequest(
            "PATCH", f"/cluster/{service_group_instance_no}/dataNodeCount", json=body
        )

    # --- Monitoring ---

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

    def get_node_metrics(
        self,
        service_group_instance_no: str,
        node_no: str,
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
            f"/cluster/{service_group_instance_no}/node/{node_no}/metrics",
            json=body if body else None,
        )

    async def aget_node_metrics(
        self,
        service_group_instance_no: str,
        node_no: str,
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
            f"/cluster/{service_group_instance_no}/node/{node_no}/metrics",
            json=body if body else None,
        )

    # --- Snapshots ---

    def get_snapshot_list(self, service_group_instance_no: str) -> dict[str, Any]:
        return self.request("GET", f"/cluster/{service_group_instance_no}/snapshot")

    async def aget_snapshot_list(
        self, service_group_instance_no: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/cluster/{service_group_instance_no}/snapshot"
        )

    def create_snapshot(
        self, service_group_instance_no: str, *, snapshot_name: str
    ) -> dict[str, Any]:
        return self.request(
            "POST",
            f"/cluster/{service_group_instance_no}/snapshot",
            json={"snapshotName": snapshot_name},
        )

    async def acreate_snapshot(
        self, service_group_instance_no: str, *, snapshot_name: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "POST",
            f"/cluster/{service_group_instance_no}/snapshot",
            json={"snapshotName": snapshot_name},
        )

    def delete_snapshot(
        self, service_group_instance_no: str, snapshot_name: str
    ) -> dict[str, Any]:
        return self.request(
            "DELETE", f"/cluster/{service_group_instance_no}/snapshot/{snapshot_name}"
        )

    async def adelete_snapshot(
        self, service_group_instance_no: str, snapshot_name: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "DELETE", f"/cluster/{service_group_instance_no}/snapshot/{snapshot_name}"
        )

    def restore_snapshot(
        self, service_group_instance_no: str, snapshot_name: str
    ) -> dict[str, Any]:
        return self.request(
            "POST",
            f"/cluster/{service_group_instance_no}/snapshot/{snapshot_name}/restore",
        )

    async def arestore_snapshot(
        self, service_group_instance_no: str, snapshot_name: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "POST",
            f"/cluster/{service_group_instance_no}/snapshot/{snapshot_name}/restore",
        )

    # --- Import data ---

    def get_import_status(self, service_group_instance_no: str) -> dict[str, Any]:
        return self.request("GET", f"/cluster/{service_group_instance_no}/import")

    async def aget_import_status(
        self, service_group_instance_no: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/cluster/{service_group_instance_no}/import"
        )

    def start_import(
        self, service_group_instance_no: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return self.request(
            "POST", f"/cluster/{service_group_instance_no}/import", json=body
        )

    async def astart_import(
        self, service_group_instance_no: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.arequest(
            "POST", f"/cluster/{service_group_instance_no}/import", json=body
        )

    # --- Metadata ---

    def get_ses_version_list(self) -> dict[str, Any]:
        return self.request("GET", "/sesVersion")

    async def aget_ses_version_list(self) -> dict[str, Any]:
        return await self.arequest("GET", "/sesVersion")

    def get_node_product_list(
        self, *, ses_version_id: str | None = None, node_type: str | None = None
    ) -> dict[str, Any]:
        params = _body(sesVersionId=ses_version_id, nodeType=node_type)
        return self.request("GET", "/nodeProduct", params=params if params else None)

    async def aget_node_product_list(
        self, *, ses_version_id: str | None = None, node_type: str | None = None
    ) -> dict[str, Any]:
        params = _body(sesVersionId=ses_version_id, nodeType=node_type)
        return await self.arequest(
            "GET", "/nodeProduct", params=params if params else None
        )

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

    def get_object_storage_bucket_list(self) -> dict[str, Any]:
        return self.request("GET", "/objectStorage/bucket")

    async def aget_object_storage_bucket_list(self) -> dict[str, Any]:
        return await self.arequest("GET", "/objectStorage/bucket")

    def get_object_storage_bucket_objects(self, bucket_name: str) -> dict[str, Any]:
        return self.request("GET", f"/objectStorage/bucket/{bucket_name}")

    async def aget_object_storage_bucket_objects(
        self, bucket_name: str
    ) -> dict[str, Any]:
        return await self.arequest("GET", f"/objectStorage/bucket/{bucket_name}")
