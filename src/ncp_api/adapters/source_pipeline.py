from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

SOURCE_PIPELINE_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://sourcepipeline.apigw.ntruss.com",
    NcpEnv.GOV: "https://sourcepipeline.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://sourcepipeline.apigw.fin-ntruss.com",
}

VPC_SOURCE_PIPELINE_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://vpcsourcepipeline.apigw.ntruss.com",
    NcpEnv.GOV: "https://vpcsourcepipeline.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://vpcsourcepipeline.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class SourcePipelineApi(NcpHttpAdapter):
    """Source Pipeline (sourcepipeline/vsourcepipeline). Signature v1, REST API."""

    path_prefix: ClassVar[str] = "/api/v1"
    _signature_version: ClassVar[str] = "v1"

    # --- Projects ---

    def get_projects(self) -> dict[str, Any]:
        return self.request("GET", "/project")

    async def aget_projects(self) -> dict[str, Any]:
        return await self.arequest("GET", "/project")

    def get_project(self, project_id: str) -> dict[str, Any]:
        return self.request("GET", f"/project/{project_id}")

    async def aget_project(self, project_id: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/project/{project_id}")

    def create_project(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create a pipeline project. body follows the CreateProject schema."""
        return self.request("POST", "/project", json=body)

    async def acreate_project(self, body: dict[str, Any]) -> dict[str, Any]:
        return await self.arequest("POST", "/project", json=body)

    def change_project(self, project_id: str, body: dict[str, Any]) -> dict[str, Any]:
        """Update a pipeline project. body follows the ChangeProject schema."""
        return self.request("PATCH", f"/project/{project_id}", json=body)

    async def achange_project(
        self, project_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.arequest("PATCH", f"/project/{project_id}", json=body)

    def delete_project(self, project_id: str) -> dict[str, Any]:
        return self.request("DELETE", f"/project/{project_id}")

    async def adelete_project(self, project_id: str) -> dict[str, Any]:
        return await self.arequest("DELETE", f"/project/{project_id}")

    # --- Pipeline execution ---

    def start_project(self, project_id: str) -> dict[str, Any]:
        return self.request("POST", f"/project/{project_id}/do")

    async def astart_project(self, project_id: str) -> dict[str, Any]:
        return await self.arequest("POST", f"/project/{project_id}/do")

    # --- History ---

    def get_project_histories(self, project_id: str) -> dict[str, Any]:
        return self.request("GET", f"/project/{project_id}/history")

    async def aget_project_histories(self, project_id: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/project/{project_id}/history")

    def get_project_history(self, project_id: str, history_id: str) -> dict[str, Any]:
        return self.request("GET", f"/project/{project_id}/history/{history_id}")

    async def aget_project_history(
        self, project_id: str, history_id: str
    ) -> dict[str, Any]:
        return await self.arequest("GET", f"/project/{project_id}/history/{history_id}")

    def cancel_project(self, project_id: str, history_id: str) -> dict[str, Any]:
        return self.request(
            "POST", f"/project/{project_id}/history/{history_id}/cancel"
        )

    async def acancel_project(self, project_id: str, history_id: str) -> dict[str, Any]:
        return await self.arequest(
            "POST", f"/project/{project_id}/history/{history_id}/cancel"
        )

    # --- Resource helpers ---

    def get_sourcebuild_projects(self) -> dict[str, Any]:
        return self.request("GET", "/sourcebuild/project")

    async def aget_sourcebuild_projects(self) -> dict[str, Any]:
        return await self.arequest("GET", "/sourcebuild/project")

    def get_sourcecommit_repositories(self) -> dict[str, Any]:
        return self.request("GET", "/sourcecommit/repository")

    async def aget_sourcecommit_repositories(self) -> dict[str, Any]:
        return await self.arequest("GET", "/sourcecommit/repository")

    def get_sourcecommit_repository_branches(
        self, repository_name: str
    ) -> dict[str, Any]:
        return self.request("GET", f"/sourcecommit/repository/{repository_name}/branch")

    async def aget_sourcecommit_repository_branches(
        self, repository_name: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/sourcecommit/repository/{repository_name}/branch"
        )

    def get_sourcedeploy_projects(self) -> dict[str, Any]:
        return self.request("GET", "/sourcedeploy/project")

    async def aget_sourcedeploy_projects(self) -> dict[str, Any]:
        return await self.arequest("GET", "/sourcedeploy/project")

    def get_sourcedeploy_project_stages(self, project_id: str) -> dict[str, Any]:
        return self.request("GET", f"/sourcedeploy/project/{project_id}/stage")

    async def aget_sourcedeploy_project_stages(self, project_id: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/sourcedeploy/project/{project_id}/stage")

    def get_sourcedeploy_project_scenarios(
        self, project_id: str, stage_id: str
    ) -> dict[str, Any]:
        return self.request(
            "GET", f"/sourcedeploy/project/{project_id}/stage/{stage_id}/scenario"
        )

    async def aget_sourcedeploy_project_scenarios(
        self, project_id: str, stage_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/sourcedeploy/project/{project_id}/stage/{stage_id}/scenario"
        )

    def get_time_zone(self) -> dict[str, Any]:
        return self.request("GET", "/trigger/timezone")

    async def aget_time_zone(self) -> dict[str, Any]:
        return await self.arequest("GET", "/trigger/timezone")
