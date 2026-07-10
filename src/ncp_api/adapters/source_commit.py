from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

SOURCE_COMMIT_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://sourcecommit.apigw.ntruss.com",
    NcpEnv.GOV: "https://sourcecommit.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://sourcecommit.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class SourceCommitApi(NcpHttpAdapter):
    """Source Commit (sourcecommit). Uses signature v1, REST API with JSON bodies."""

    path_prefix: ClassVar[str] = "/api/v1"
    _signature_version: ClassVar[str] = "v1"

    def get_repositories(
        self,
        *,
        page_no: int | None = None,
        page_size: int | None = None,
        project_name: str | None = None,
    ) -> dict[str, Any]:
        params = _body(pageNo=page_no, pageSize=page_size, projectName=project_name)
        return self.request("GET", "/repository", params=params if params else None)

    async def aget_repositories(
        self,
        *,
        page_no: int | None = None,
        page_size: int | None = None,
        project_name: str | None = None,
    ) -> dict[str, Any]:
        params = _body(pageNo=page_no, pageSize=page_size, projectName=project_name)
        return await self.arequest(
            "GET", "/repository", params=params if params else None
        )

    def get_repository(self, repository_name: str) -> dict[str, Any]:
        return self.request("GET", f"/repository/{repository_name}")

    async def aget_repository(self, repository_name: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/repository/{repository_name}")

    def get_repository_by_id(self, repository_id: str) -> dict[str, Any]:
        return self.request("GET", f"/repository/id/{repository_id}")

    async def aget_repository_by_id(self, repository_id: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/repository/id/{repository_id}")

    def create_repository(
        self,
        *,
        name: str,
        description: str | None = None,
        linked: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        body = _body(name=name, description=description, linked=linked)
        return self.request("POST", "/repository", json=body)

    async def acreate_repository(
        self,
        *,
        name: str,
        description: str | None = None,
        linked: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        body = _body(name=name, description=description, linked=linked)
        return await self.arequest("POST", "/repository", json=body)

    def delete_repository(self, repository_id: str) -> dict[str, Any]:
        return self.request("DELETE", f"/repository/id/{repository_id}")

    async def adelete_repository(self, repository_id: str) -> dict[str, Any]:
        return await self.arequest("DELETE", f"/repository/id/{repository_id}")

    def change_repository(
        self,
        repository_id: str,
        *,
        description: str | None = None,
        linked: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        body = _body(description=description, linked=linked)
        return self.request("PATCH", f"/repository/id/{repository_id}", json=body)

    async def achange_repository(
        self,
        repository_id: str,
        *,
        description: str | None = None,
        linked: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        body = _body(description=description, linked=linked)
        return await self.arequest(
            "PATCH", f"/repository/id/{repository_id}", json=body
        )
