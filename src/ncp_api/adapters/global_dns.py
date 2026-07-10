from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

GLOBAL_DNS_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://globaldns.apigw.ntruss.com",
    NcpEnv.GOV: "https://globaldns.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://globaldns.apigw.fin-ntruss.com",
}


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


class GlobalDnsApi(NcpHttpAdapter):
    path_prefix: ClassVar[str] = "/dns/v1/ncpdns"

    def get_domain_list(
        self,
        *,
        page: int = 0,
        size: int = 20,
        domain_name: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(page=page, size=size, domainName=domain_name)
        result: dict[str, Any] = self.request("GET", "/domain", params=params)
        return result

    async def aget_domain_list(
        self,
        *,
        page: int = 0,
        size: int = 20,
        domain_name: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(page=page, size=size, domainName=domain_name)
        result: dict[str, Any] = await self.arequest("GET", "/domain", params=params)
        return result

    def get_record_list(
        self,
        domain_id: int,
        *,
        page: int = 0,
        size: int = 20,
        record_type: str | None = None,
        search_content: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            page=page,
            size=size,
            recordType=record_type,
            searchContent=search_content,
        )
        result: dict[str, Any] = self.request(
            "GET", f"/record/{domain_id}", params=params
        )
        return result

    async def aget_record_list(
        self,
        domain_id: int,
        *,
        page: int = 0,
        size: int = 20,
        record_type: str | None = None,
        search_content: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            page=page,
            size=size,
            recordType=record_type,
            searchContent=search_content,
        )
        result: dict[str, Any] = await self.arequest(
            "GET", f"/record/{domain_id}", params=params
        )
        return result
