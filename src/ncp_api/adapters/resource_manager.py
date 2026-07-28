from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

RESOURCE_MANAGER_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://resourcemanager.apigw.ntruss.com",
    NcpEnv.GOV: "https://resourcemanager.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://resourcemanager.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class ResourceManagerApi(NcpHttpAdapter):
    """Resource Manager. Sig-v2, REST + JSON."""

    path_prefix: ClassVar[str] = "/api/v1"

    def get_resource_list(
        self,
        *,
        nrn: str | None = None,
        product_name: str | None = None,
        region_code: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        resource_name: str | None = None,
        tag: list[dict[str, str]] | None = None,
        group_name: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> dict[str, Any]:
        body = _body(
            nrn=nrn,
            productName=product_name,
            regionCode=region_code,
            resourceType=resource_type,
            resourceId=resource_id,
            resourceName=resource_name,
            tag=tag,
            groupName=group_name,
            page=page,
            size=size,
        )
        return self.request("POST", "/resources", json=body)

    async def aget_resource_list(
        self,
        *,
        nrn: str | None = None,
        product_name: str | None = None,
        region_code: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        resource_name: str | None = None,
        tag: list[dict[str, str]] | None = None,
        group_name: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> dict[str, Any]:
        body = _body(
            nrn=nrn,
            productName=product_name,
            regionCode=region_code,
            resourceType=resource_type,
            resourceId=resource_id,
            resourceName=resource_name,
            tag=tag,
            groupName=group_name,
            page=page,
            size=size,
        )
        return await self.arequest("POST", "/resources", json=body)
