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


class SubAccountApi(NcpHttpAdapter):
    """Sub Account (IAM policy). Sig-v2, REST + JSON."""

    path_prefix: ClassVar[str] = "/api/v1"

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
