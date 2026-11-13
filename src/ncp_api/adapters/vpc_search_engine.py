from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

VPC_SEARCH_ENGINE_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://vpcsearchengine.apigw.ntruss.com",
    NcpEnv.GOV: "https://vpcsearchengine.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://vpcsearchengine.apigw.fin-ntruss.com",
}


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


class VpcSearchEngineApi(NcpHttpAdapter):
    """VPC Search Engine Service clusters. Sig-v2, REST + JSON.

    Response envelope: {code, message, result, requestId}. `api_version`
    selects region: "v2" for 수도권 (default), "krs-v2" for 남부권.
    """

    path_prefix: ClassVar[str] = ""

    def get_cluster_info_list(
        self,
        *,
        api_version: str = "v2",
        input_text: str | None = None,
        vpc_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            inputText=input_text,
            vpcName=vpc_name,
            pageNo=page_no,
            pageSize=page_size,
        )
        raw = self.request(
            "GET", f"/api/{api_version}/cluster/getClusterInfoList", params=params
        )
        result: dict[str, Any] = raw["result"]
        return result

    async def aget_cluster_info_list(
        self,
        *,
        api_version: str = "v2",
        input_text: str | None = None,
        vpc_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            inputText=input_text,
            vpcName=vpc_name,
            pageNo=page_no,
            pageSize=page_size,
        )
        raw = await self.arequest(
            "GET", f"/api/{api_version}/cluster/getClusterInfoList", params=params
        )
        result: dict[str, Any] = raw["result"]
        return result

    def get_cluster_node_list(
        self,
        *,
        service_group_instance_no: str,
        api_version: str = "v2",
    ) -> dict[str, Any]:
        raw = self.request(
            "GET",
            f"/api/{api_version}/cluster/getClusterNodeList/{service_group_instance_no}",
        )
        result: dict[str, Any] = raw["result"]
        return result

    async def aget_cluster_node_list(
        self,
        *,
        service_group_instance_no: str,
        api_version: str = "v2",
    ) -> dict[str, Any]:
        raw = await self.arequest(
            "GET",
            f"/api/{api_version}/cluster/getClusterNodeList/{service_group_instance_no}",
        )
        result: dict[str, Any] = raw["result"]
        return result
