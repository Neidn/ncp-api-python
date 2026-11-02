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


def _list_sub_accounts_params(
    *,
    page_no: int | None,
    page_size: int | None,
    sort: list[str] | None,
) -> list[tuple[str, str]]:
    params: list[tuple[str, str]] = []
    if page_no is not None:
        params.append(("pageNo", str(page_no)))
    if page_size is not None:
        params.append(("pageSize", str(page_size)))
    if sort:
        params.extend(("sort", s) for s in sort)
    return params


class SubAccountApiV2(NcpHttpAdapter):
    """Sub Account (IAM v2 -- Ncloud API standard spec). Sig-v2, REST + JSON.

    First style of NCP's newer standardized API spec (rolled out in gov
    zone first): clean resource paths (GET /users/{id}) under /api/v2,
    same sig-v2 HMAC auth and domain as the v1 SubAccountApi above.
    """

    path_prefix: ClassVar[str] = "/api/v2"

    def get_user(self, *, sub_account_id: str) -> dict[str, Any]:
        return self.request("GET", f"/users/{sub_account_id}")

    async def aget_user(self, *, sub_account_id: str) -> dict[str, Any]:
        return await self.arequest("GET", f"/users/{sub_account_id}")

    def list_sub_accounts(
        self,
        *,
        page_no: int | None = None,
        page_size: int | None = None,
        sort: list[str] | None = None,
    ) -> dict[str, Any]:
        params = _list_sub_accounts_params(
            page_no=page_no, page_size=page_size, sort=sort
        )
        return self.request("GET", "/sub-accounts", params=params)

    async def alist_sub_accounts(
        self,
        *,
        page_no: int | None = None,
        page_size: int | None = None,
        sort: list[str] | None = None,
    ) -> dict[str, Any]:
        params = _list_sub_accounts_params(
            page_no=page_no, page_size=page_size, sort=sort
        )
        return await self.arequest("GET", "/sub-accounts", params=params)
