from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

SUBACCOUNT_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://subaccount.apigw.ntruss.com",
    NcpEnv.GOV: "https://subaccount.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://subaccount.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


class SubAccountApi(NcpHttpAdapter):
    """Sub Account (IAM policy). Sig-v2, REST + JSON."""

    path_prefix: ClassVar[str] = "/api/v1"

    def get_sub_accounts(
        self,
        *,
        search_column: str | None = None,
        search_word: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            searchColumn=search_column,
            searchWord=search_word,
            page=page,
            size=size,
        )
        return self.request("GET", "/sub-accounts", params=params)

    async def aget_sub_accounts(
        self,
        *,
        search_column: str | None = None,
        search_word: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            searchColumn=search_column,
            searchWord=search_word,
            page=page,
            size=size,
        )
        return await self.arequest("GET", "/sub-accounts", params=params)

    # permissions[].targets[].product is a service code; the valid set
    # differs per environment and changes over time (see
    # guide.ncloud-docs.com/docs/subaccount-servicelist, or the -gov variant).
    def create_policy(
        self,
        *,
        policy_name: str,
        permissions: list[dict[str, Any]],
        description: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        body = _body(
            policyName=policy_name,
            permissions=permissions,
            description=description,
            tags=tags,
        )
        return self.request("POST", "/policies", json=body)

    async def acreate_policy(
        self,
        *,
        policy_name: str,
        permissions: list[dict[str, Any]],
        description: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        body = _body(
            policyName=policy_name,
            permissions=permissions,
            description=description,
            tags=tags,
        )
        return await self.arequest("POST", "/policies", json=body)
