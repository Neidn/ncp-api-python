from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

CLOUD_LOG_ANALYTICS_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://cloudloganalytics.apigw.ntruss.com",
    NcpEnv.GOV: "https://cloudloganalytics.apigw.gov-ntruss.com",
    # TBD: confirm from fin docs
    NcpEnv.FIN: "https://cloudloganalytics.apigw.fin-ntruss.com",
}


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


class CloudLogAnalyticsApi(NcpHttpAdapter):
    """Cloud Log Analytics (VPC server-list + log-collection status). Sig-v2, REST+JSON.

    Each method lists VPC resources of one product type and their Cloud Log
    Analytics collection status. Response envelope: {code, message, result}.
    """

    path_prefix: ClassVar[str] = ""

    def _get_server_list(
        self,
        *,
        suffix: str,
        region_code: str,
        page_no: int | None,
        page_size: int | None,
    ) -> dict[str, Any]:
        params = _build_params(pageNo=page_no, pageSize=page_size)
        raw = self.request(
            "GET", f"/api/{region_code}-v1/vpc/servers{suffix}", params=params
        )
        result: dict[str, Any] = raw["result"]
        return result

    async def _aget_server_list(
        self,
        *,
        suffix: str,
        region_code: str,
        page_no: int | None,
        page_size: int | None,
    ) -> dict[str, Any]:
        params = _build_params(pageNo=page_no, pageSize=page_size)
        raw = await self.arequest(
            "GET", f"/api/{region_code}-v1/vpc/servers{suffix}", params=params
        )
        result: dict[str, Any] = raw["result"]
        return result

    # result.vpcServerInfos + result.collectingCount
    def get_vpc_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return self._get_server_list(
            suffix="", region_code=region_code, page_no=page_no, page_size=page_size
        )

    async def aget_vpc_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return await self._aget_server_list(
            suffix="", region_code=region_code, page_no=page_no, page_size=page_size
        )

    # result.dbServers
    def get_vpc_mysql_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return self._get_server_list(
            suffix="/mysql",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    async def aget_vpc_mysql_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return await self._aget_server_list(
            suffix="/mysql",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    # result.dbServers
    def get_vpc_mssql_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return self._get_server_list(
            suffix="/mssql",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    async def aget_vpc_mssql_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return await self._aget_server_list(
            suffix="/mssql",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    # result.dbServers
    def get_vpc_mongodb_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return self._get_server_list(
            suffix="/mongodb",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    async def aget_vpc_mongodb_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return await self._aget_server_list(
            suffix="/mongodb",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    # result.dbServers
    def get_vpc_postgresql_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return self._get_server_list(
            suffix="/postgresql",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    async def aget_vpc_postgresql_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return await self._aget_server_list(
            suffix="/postgresql",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    # result.dbServers
    def get_vpc_baremetal_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return self._get_server_list(
            suffix="/baremetal",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    async def aget_vpc_baremetal_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return await self._aget_server_list(
            suffix="/baremetal",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    # result.clusters -- wire path is /vpc/servers/kubernetes, not /nks
    def get_vpc_nks_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return self._get_server_list(
            suffix="/kubernetes",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    async def aget_vpc_nks_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return await self._aget_server_list(
            suffix="/kubernetes",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    # result.clusters
    def get_vpc_ses_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return self._get_server_list(
            suffix="/ses",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    async def aget_vpc_ses_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return await self._aget_server_list(
            suffix="/ses",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    # result.clusterInfoList
    def get_vpc_cdss_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return self._get_server_list(
            suffix="/cdss",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )

    async def aget_vpc_cdss_server_list(
        self,
        *,
        region_code: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        return await self._aget_server_list(
            suffix="/cdss",
            region_code=region_code,
            page_no=page_no,
            page_size=page_size,
        )
