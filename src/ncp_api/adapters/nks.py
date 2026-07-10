from __future__ import annotations

from typing import Any, ClassVar, cast

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

NKS_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://nks.apigw.ntruss.com",
    NcpEnv.GOV: "https://nks.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://nks.apigw.fin-ntruss.com",
}

_REGION_PATH_PREFIX: dict[str, str] = {
    "KR": "/vnks/v2",
    "KRS": "/vnks/krs-v2",  # Busan — gov only
    "SGN": "/vnks/sgn-v2",
    "JPN": "/vnks/jpn-v2",
}


class NksApi(NcpHttpAdapter):
    path_prefix: ClassVar[str] = ""

    def get_cluster_list(self, *, region_code: str = "KR") -> list[dict[str, Any]]:
        prefix = _REGION_PATH_PREFIX.get(region_code.upper(), "/vnks/v2")
        raw = self.request("GET", f"{prefix}/clusters")
        return cast(list[dict[str, Any]], raw["clusters"])

    async def aget_cluster_list(
        self, *, region_code: str = "KR"
    ) -> list[dict[str, Any]]:
        prefix = _REGION_PATH_PREFIX.get(region_code.upper(), "/vnks/v2")
        raw = await self.arequest("GET", f"{prefix}/clusters")
        return cast(list[dict[str, Any]], raw["clusters"])

    def get_worker_nodes(
        self, uuid: str, *, region_code: str = "KR"
    ) -> list[dict[str, Any]]:
        prefix = _REGION_PATH_PREFIX.get(region_code.upper(), "/vnks/v2")
        raw = self.request("GET", f"{prefix}/clusters/{uuid}/nodes")
        return cast(list[dict[str, Any]], raw["nodes"])

    async def aget_worker_nodes(
        self, uuid: str, *, region_code: str = "KR"
    ) -> list[dict[str, Any]]:
        prefix = _REGION_PATH_PREFIX.get(region_code.upper(), "/vnks/v2")
        raw = await self.arequest("GET", f"{prefix}/clusters/{uuid}/nodes")
        return cast(list[dict[str, Any]], raw["nodes"])

    def get_node_pool(
        self,
        uuid: str,
        *,
        hypervisor_code: str | None = None,
        region_code: str = "KR",
    ) -> list[dict[str, Any]]:
        prefix = _REGION_PATH_PREFIX.get(region_code.upper(), "/vnks/v2")
        params: dict[str, str] = {}
        if hypervisor_code is not None:
            params["hypervisorCode"] = hypervisor_code
        raw = self.request(
            "GET", f"{prefix}/clusters/{uuid}/node-pool", params=params or None
        )
        return cast(list[dict[str, Any]], raw["nodePool"])

    async def aget_node_pool(
        self,
        uuid: str,
        *,
        hypervisor_code: str | None = None,
        region_code: str = "KR",
    ) -> list[dict[str, Any]]:
        prefix = _REGION_PATH_PREFIX.get(region_code.upper(), "/vnks/v2")
        params: dict[str, str] = {}
        if hypervisor_code is not None:
            params["hypervisorCode"] = hypervisor_code
        raw = await self.arequest(
            "GET", f"{prefix}/clusters/{uuid}/node-pool", params=params or None
        )
        return cast(list[dict[str, Any]], raw["nodePool"])
