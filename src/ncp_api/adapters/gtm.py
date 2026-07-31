from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

GTM_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://globaltrafficmanager.apigw.ntruss.com",
    NcpEnv.GOV: "https://globaltrafficmanager.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://globaltrafficmanager.apigw.fin-ntruss.com",
}


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


class GtmApi(NcpHttpAdapter):
    """Global Traffic Manager. Sig-v2, REST + JSON."""

    path_prefix: ClassVar[str] = "/gtm/v1"

    def get_profile_list(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(page=page, size=size, name=name)
        return self.request("GET", "/domains", params=params)

    async def aget_profile_list(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(page=page, size=size, name=name)
        return await self.arequest("GET", "/domains", params=params)

    def get_policy_list(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        apply_yn: bool | None = None,
        domain_name: str | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            page=page,
            size=size,
            applyYn=apply_yn,
            domainName=domain_name,
            name=name,
        )
        return self.request("GET", "/policies", params=params)

    async def aget_policy_list(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        apply_yn: bool | None = None,
        domain_name: str | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            page=page,
            size=size,
            applyYn=apply_yn,
            domainName=domain_name,
            name=name,
        )
        return await self.arequest("GET", "/policies", params=params)
