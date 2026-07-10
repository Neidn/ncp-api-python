from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

VPC_SOURCE_DEPLOY_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://vpcsourcedeploy.apigw.ntruss.com",
    NcpEnv.GOV: "https://vpcsourcedeploy.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://vpcsourcedeploy.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class VpcSourceDeployApi(NcpHttpAdapter):
    """VPC Source Deploy (vsourcedeploy). Signature v1, REST API with JSON bodies."""

    path_prefix: ClassVar[str] = "/api/v1"
    _signature_version: ClassVar[str] = "v1"

    # --- Resource helpers ---

    def get_autoscaling_groups(self) -> dict[str, Any]:
        return self.request("GET", "/autoscaling")

    async def aget_autoscaling_groups(self) -> dict[str, Any]:
        return await self.arequest("GET", "/autoscaling")

    def get_autoscaling_group_target_group(
        self, autoscaling_name: str
    ) -> dict[str, Any]:
        return self.request("GET", f"/autoscaling/{autoscaling_name}")

    async def aget_autoscaling_group_target_group(
        self, autoscaling_name: str
    ) -> dict[str, Any]:
        return await self.arequest("GET", f"/autoscaling/{autoscaling_name}")

    def get_kubernetes_clusters(self) -> dict[str, Any]:
        return self.request("GET", "/kubernetes/cluster")

    async def aget_kubernetes_clusters(self) -> dict[str, Any]:
        return await self.arequest("GET", "/kubernetes/cluster")

    def get_objectstorage_buckets(self) -> dict[str, Any]:
        return self.request("GET", "/objectstorage/bucket")

    async def aget_objectstorage_buckets(self) -> dict[str, Any]:
        return await self.arequest("GET", "/objectstorage/bucket")

    def get_objectstorage_objects(self, bucket_name: str) -> dict[str, Any]:
        return self.request("GET", f"/objectstorage/bucket/{bucket_name}")

    async def aget_objectstorage_objects(self, bucket_name: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/objectstorage/bucket/{bucket_name}")

    def get_servers(self) -> dict[str, Any]:
        return self.request("GET", "/server")

    async def aget_servers(self) -> dict[str, Any]:
        return await self.arequest("GET", "/server")

    def get_sourcebuild_projects(self) -> dict[str, Any]:
        return self.request("GET", "/sourcebuild/project")

    async def aget_sourcebuild_projects(self) -> dict[str, Any]:
        return await self.arequest("GET", "/sourcebuild/project")

    def get_sourcecommit_repositories(self) -> dict[str, Any]:
        return self.request("GET", "/sourcecommit/repository")

    async def aget_sourcecommit_repositories(self) -> dict[str, Any]:
        return await self.arequest("GET", "/sourcecommit/repository")

    def get_sourcecommit_branches(self, repository_name: str) -> dict[str, Any]:
        return self.request("GET", f"/sourcecommit/repository/{repository_name}/branch")

    async def aget_sourcecommit_branches(self, repository_name: str) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/sourcecommit/repository/{repository_name}/branch"
        )

    # --- Projects ---

    def get_projects(
        self,
        *,
        page_no: str | None = None,
        page_size: str | None = None,
        project_name: str | None = None,
    ) -> dict[str, Any]:
        params = _body(pageNo=page_no, pageSize=page_size, projectName=project_name)
        return self.request("GET", "/project", params=params if params else None)

    async def aget_projects(
        self,
        *,
        page_no: str | None = None,
        page_size: str | None = None,
        project_name: str | None = None,
    ) -> dict[str, Any]:
        params = _body(pageNo=page_no, pageSize=page_size, projectName=project_name)
        return await self.arequest("GET", "/project", params=params if params else None)

    def create_project(self, *, name: str) -> dict[str, Any]:
        return self.request("POST", "/project", json={"name": name})

    async def acreate_project(self, *, name: str) -> dict[str, Any]:
        return await self.arequest("POST", "/project", json={"name": name})

    def delete_project(self, project_id: str) -> dict[str, Any]:
        return self.request("DELETE", f"/project/{project_id}")

    async def adelete_project(self, project_id: str) -> dict[str, Any]:
        return await self.arequest("DELETE", f"/project/{project_id}")

    # --- Deploy History ---

    def get_histories(
        self,
        project_id: str,
        *,
        page_no: str | None = None,
        page_size: str | None = None,
    ) -> dict[str, Any]:
        params = _body(pageNo=page_no, pageSize=page_size)
        return self.request(
            "GET", f"/project/{project_id}/history", params=params if params else None
        )

    async def aget_histories(
        self,
        project_id: str,
        *,
        page_no: str | None = None,
        page_size: str | None = None,
    ) -> dict[str, Any]:
        params = _body(pageNo=page_no, pageSize=page_size)
        return await self.arequest(
            "GET", f"/project/{project_id}/history", params=params if params else None
        )

    def get_history(self, project_id: str, history_id: str) -> dict[str, Any]:
        return self.request("GET", f"/project/{project_id}/history/{history_id}")

    async def aget_history(self, project_id: str, history_id: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/project/{project_id}/history/{history_id}")

    def accept_deploy_approval(
        self, project_id: str, history_id: str
    ) -> dict[str, Any]:
        return self.request(
            "POST", f"/project/{project_id}/history/{history_id}/approval/accept"
        )

    async def aaccept_deploy_approval(
        self, project_id: str, history_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "POST", f"/project/{project_id}/history/{history_id}/approval/accept"
        )

    def reject_deploy_approval(
        self, project_id: str, history_id: str
    ) -> dict[str, Any]:
        return self.request(
            "POST", f"/project/{project_id}/history/{history_id}/approval/reject"
        )

    async def areject_deploy_approval(
        self, project_id: str, history_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "POST", f"/project/{project_id}/history/{history_id}/approval/reject"
        )

    def accept_deploy_canary(self, project_id: str, history_id: str) -> dict[str, Any]:
        return self.request(
            "POST", f"/project/{project_id}/history/{history_id}/canary/accept"
        )

    async def aaccept_deploy_canary(
        self, project_id: str, history_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "POST", f"/project/{project_id}/history/{history_id}/canary/accept"
        )

    def reject_deploy_canary(self, project_id: str, history_id: str) -> dict[str, Any]:
        return self.request(
            "POST", f"/project/{project_id}/history/{history_id}/canary/reject"
        )

    async def areject_deploy_canary(
        self, project_id: str, history_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "POST", f"/project/{project_id}/history/{history_id}/canary/reject"
        )

    def cancel_deploy(self, project_id: str, history_id: str) -> dict[str, Any]:
        return self.request(
            "POST", f"/project/{project_id}/history/{history_id}/cancel"
        )

    async def acancel_deploy(self, project_id: str, history_id: str) -> dict[str, Any]:
        return await self.arequest(
            "POST", f"/project/{project_id}/history/{history_id}/cancel"
        )

    def get_canary_report_endtime(
        self, project_id: str, history_id: str
    ) -> dict[str, Any]:
        return self.request("GET", f"/project/{project_id}/history/{history_id}/report")

    async def aget_canary_report_endtime(
        self, project_id: str, history_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/project/{project_id}/history/{history_id}/report"
        )

    def get_canary_report(
        self, project_id: str, history_id: str, endtime: str
    ) -> dict[str, Any]:
        return self.request(
            "GET", f"/project/{project_id}/history/{history_id}/report/{endtime}"
        )

    async def aget_canary_report(
        self, project_id: str, history_id: str, endtime: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/project/{project_id}/history/{history_id}/report/{endtime}"
        )

    # --- Stages ---

    def get_stages(
        self,
        project_id: str,
        *,
        page_no: str | None = None,
        page_size: str | None = None,
        stage_name: str | None = None,
    ) -> dict[str, Any]:
        params = _body(pageNo=page_no, pageSize=page_size, stageName=stage_name)
        return self.request(
            "GET", f"/project/{project_id}/stage", params=params if params else None
        )

    async def aget_stages(
        self,
        project_id: str,
        *,
        page_no: str | None = None,
        page_size: str | None = None,
        stage_name: str | None = None,
    ) -> dict[str, Any]:
        params = _body(pageNo=page_no, pageSize=page_size, stageName=stage_name)
        return await self.arequest(
            "GET", f"/project/{project_id}/stage", params=params if params else None
        )

    def get_stage(self, project_id: str, stage_id: str) -> dict[str, Any]:
        return self.request("GET", f"/project/{project_id}/stage/{stage_id}")

    async def aget_stage(self, project_id: str, stage_id: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/project/{project_id}/stage/{stage_id}")

    def create_stage(self, project_id: str, body: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", f"/project/{project_id}/stage", json=body)

    async def acreate_stage(
        self, project_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.arequest("POST", f"/project/{project_id}/stage", json=body)

    def change_stage(
        self, project_id: str, stage_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return self.request(
            "PATCH", f"/project/{project_id}/stage/{stage_id}", json=body
        )

    async def achange_stage(
        self, project_id: str, stage_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.arequest(
            "PATCH", f"/project/{project_id}/stage/{stage_id}", json=body
        )

    def delete_stage(self, project_id: str, stage_id: str) -> dict[str, Any]:
        return self.request("DELETE", f"/project/{project_id}/stage/{stage_id}")

    async def adelete_stage(self, project_id: str, stage_id: str) -> dict[str, Any]:
        return await self.arequest("DELETE", f"/project/{project_id}/stage/{stage_id}")

    # --- Scenarios ---

    def get_scenarios(
        self,
        project_id: str,
        stage_id: str,
        *,
        page_no: str | None = None,
        page_size: str | None = None,
        scenario_name: str | None = None,
    ) -> dict[str, Any]:
        params = _body(pageNo=page_no, pageSize=page_size, scenarioName=scenario_name)
        return self.request(
            "GET",
            f"/project/{project_id}/stage/{stage_id}/scenario",
            params=params if params else None,
        )

    async def aget_scenarios(
        self,
        project_id: str,
        stage_id: str,
        *,
        page_no: str | None = None,
        page_size: str | None = None,
        scenario_name: str | None = None,
    ) -> dict[str, Any]:
        params = _body(pageNo=page_no, pageSize=page_size, scenarioName=scenario_name)
        return await self.arequest(
            "GET",
            f"/project/{project_id}/stage/{stage_id}/scenario",
            params=params if params else None,
        )

    def get_scenario(
        self, project_id: str, stage_id: str, scenario_id: str
    ) -> dict[str, Any]:
        return self.request(
            "GET", f"/project/{project_id}/stage/{stage_id}/scenario/{scenario_id}"
        )

    async def aget_scenario(
        self, project_id: str, stage_id: str, scenario_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/project/{project_id}/stage/{stage_id}/scenario/{scenario_id}"
        )

    def create_scenario(
        self, project_id: str, stage_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return self.request(
            "POST", f"/project/{project_id}/stage/{stage_id}/scenario", json=body
        )

    async def acreate_scenario(
        self, project_id: str, stage_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.arequest(
            "POST", f"/project/{project_id}/stage/{stage_id}/scenario", json=body
        )

    def change_scenario(
        self, project_id: str, stage_id: str, scenario_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return self.request(
            "PATCH",
            f"/project/{project_id}/stage/{stage_id}/scenario/{scenario_id}",
            json=body,
        )

    async def achange_scenario(
        self, project_id: str, stage_id: str, scenario_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.arequest(
            "PATCH",
            f"/project/{project_id}/stage/{stage_id}/scenario/{scenario_id}",
            json=body,
        )

    def delete_scenario(
        self, project_id: str, stage_id: str, scenario_id: str
    ) -> dict[str, Any]:
        return self.request(
            "DELETE", f"/project/{project_id}/stage/{stage_id}/scenario/{scenario_id}"
        )

    async def adelete_scenario(
        self, project_id: str, stage_id: str, scenario_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "DELETE", f"/project/{project_id}/stage/{stage_id}/scenario/{scenario_id}"
        )

    # --- Deploy actions ---

    def deploy(
        self, project_id: str, stage_id: str, scenario_id: str
    ) -> dict[str, Any]:
        return self.request(
            "POST",
            f"/project/{project_id}/stage/{stage_id}/scenario/{scenario_id}/deploy",
        )

    async def adeploy(
        self, project_id: str, stage_id: str, scenario_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "POST",
            f"/project/{project_id}/stage/{stage_id}/scenario/{scenario_id}/deploy",
        )

    def deploy_request(
        self, project_id: str, stage_id: str, scenario_id: str
    ) -> dict[str, Any]:
        return self.request(
            "POST",
            f"/project/{project_id}/stage/{stage_id}/scenario/{scenario_id}/deploy/request",
        )

    async def adeploy_request(
        self, project_id: str, stage_id: str, scenario_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "POST",
            f"/project/{project_id}/stage/{stage_id}/scenario/{scenario_id}/deploy/request",
        )
