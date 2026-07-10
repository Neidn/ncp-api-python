from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

SOURCE_BUILD_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://sourcebuild.apigw.ntruss.com",
    NcpEnv.GOV: "https://sourcebuild.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://sourcebuild.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class SourceBuildApi(NcpHttpAdapter):
    """Source Build (sourcebuild). Uses signature v1, REST API with JSON bodies."""

    path_prefix: ClassVar[str] = "/api/v1"
    _signature_version: ClassVar[str] = "v1"

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

    def get_project(self, project_id: str) -> dict[str, Any]:
        return self.request("GET", f"/project/{project_id}")

    async def aget_project(self, project_id: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/project/{project_id}")

    def create_project(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create a build project. body follows the CreateProject schema."""
        return self.request("POST", "/project", json=body)

    async def acreate_project(self, body: dict[str, Any]) -> dict[str, Any]:
        return await self.arequest("POST", "/project", json=body)

    def change_project(self, project_id: str, body: dict[str, Any]) -> dict[str, Any]:
        """Update a build project. body follows the ChangeProject schema."""
        return self.request("PATCH", f"/project/{project_id}", json=body)

    async def achange_project(
        self, project_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.arequest("PATCH", f"/project/{project_id}", json=body)

    def delete_project(self, project_id: str) -> dict[str, Any]:
        return self.request("DELETE", f"/project/{project_id}")

    async def adelete_project(self, project_id: str) -> dict[str, Any]:
        return await self.arequest("DELETE", f"/project/{project_id}")

    # --- Builds ---

    def start_build(self, project_id: str) -> dict[str, Any]:
        return self.request("POST", f"/project/{project_id}/build")

    async def astart_build(self, project_id: str) -> dict[str, Any]:
        return await self.arequest("POST", f"/project/{project_id}/build")

    def cancel_build(self, project_id: str, *, build_id: str) -> dict[str, Any]:
        return self.request(
            "DELETE", f"/project/{project_id}/build", json={"buildId": build_id}
        )

    async def acancel_build(self, project_id: str, *, build_id: str) -> dict[str, Any]:
        return await self.arequest(
            "DELETE", f"/project/{project_id}/build", json={"buildId": build_id}
        )

    def get_build_history(self, project_id: str) -> dict[str, Any]:
        return self.request("GET", f"/project/{project_id}/history")

    async def aget_build_history(self, project_id: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/project/{project_id}/history")

    # --- Environment lookups ---

    def get_compute_env(self) -> dict[str, Any]:
        return self.request("GET", "/env/compute")

    async def aget_compute_env(self) -> dict[str, Any]:
        return await self.arequest("GET", "/env/compute")

    def get_os_env(self) -> dict[str, Any]:
        return self.request("GET", "/env/os")

    async def aget_os_env(self) -> dict[str, Any]:
        return await self.arequest("GET", "/env/os")

    def get_runtime_env(self, os_id: str) -> dict[str, Any]:
        return self.request("GET", f"/env/os/{os_id}/runtime")

    async def aget_runtime_env(self, os_id: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/env/os/{os_id}/runtime")

    def get_runtime_version_env(self, os_id: str, runtime_id: str) -> dict[str, Any]:
        return self.request("GET", f"/env/os/{os_id}/runtime/{runtime_id}/version")

    async def aget_runtime_version_env(
        self, os_id: str, runtime_id: str
    ) -> dict[str, Any]:
        return await self.arequest(
            "GET", f"/env/os/{os_id}/runtime/{runtime_id}/version"
        )

    def get_docker_env(self) -> dict[str, Any]:
        return self.request("GET", "/env/docker")

    async def aget_docker_env(self) -> dict[str, Any]:
        return await self.arequest("GET", "/env/docker")

    def get_container_registry(self) -> dict[str, Any]:
        return self.request("GET", "/containerregistry/registry")

    async def aget_container_registry(self) -> dict[str, Any]:
        return await self.arequest("GET", "/containerregistry/registry")

    def get_objectstorage_bucket(self) -> dict[str, Any]:
        return self.request("GET", "/objectstorage/bucket")

    async def aget_objectstorage_bucket(self) -> dict[str, Any]:
        return await self.arequest("GET", "/objectstorage/bucket")

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
