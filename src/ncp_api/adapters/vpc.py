from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


def _list_params(key: str, values: list[str]) -> dict[str, str]:
    return {f"{key}.{i + 1}": v for i, v in enumerate(values)}


class VpcApi(NcpHttpAdapter):
    path_prefix: ClassVar[str] = "/vpc/v2"

    # --- VPC ---

    def _get_vpc_params(
        self,
        *,
        region_code: str | None,
        vpc_status_code: str | None,
        vpc_name: str | None,
        vpc_no_list: list[str] | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            vpcStatusCode=vpc_status_code,
            vpcName=vpc_name,
            responseFormatType="json",
        )
        if vpc_no_list:
            params.update(_list_params("vpcNoList", vpc_no_list))
        return params

    def get_vpc_list(
        self,
        *,
        region_code: str | None = None,
        vpc_status_code: str | None = None,
        vpc_name: str | None = None,
        vpc_no_list: list[str] | None = None,
    ) -> dict[str, Any]:
        params = self._get_vpc_params(
            region_code=region_code,
            vpc_status_code=vpc_status_code,
            vpc_name=vpc_name,
            vpc_no_list=vpc_no_list,
        )
        raw = self.request("GET", "/getVpcList", params=params)
        result: dict[str, Any] = raw["getVpcListResponse"]
        return result

    async def aget_vpc_list(
        self,
        *,
        region_code: str | None = None,
        vpc_status_code: str | None = None,
        vpc_name: str | None = None,
        vpc_no_list: list[str] | None = None,
    ) -> dict[str, Any]:
        params = self._get_vpc_params(
            region_code=region_code,
            vpc_status_code=vpc_status_code,
            vpc_name=vpc_name,
            vpc_no_list=vpc_no_list,
        )
        raw = await self.arequest("GET", "/getVpcList", params=params)
        result: dict[str, Any] = raw["getVpcListResponse"]
        return result

    # --- Subnet ---

    def _get_subnet_params(
        self,
        *,
        region_code: str | None,
        subnet_status_code: str | None,
        subnet_name: str | None,
        subnet: str | None,
        subnet_no_list: list[str] | None,
        vpc_no: str | None,
        zone_code: str | None,
        subnet_type_code: str | None,
        usage_type_code: str | None,
        network_acl_no: str | None,
        page_no: int | None,
        page_size: int | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            subnetStatusCode=subnet_status_code,
            subnetName=subnet_name,
            subnet=subnet,
            vpcNo=vpc_no,
            zoneCode=zone_code,
            subnetTypeCode=subnet_type_code,
            usageTypeCode=usage_type_code,
            networkAclNo=network_acl_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if subnet_no_list:
            params.update(_list_params("subnetNoList", subnet_no_list))
        return params

    def get_subnet_list(
        self,
        *,
        region_code: str | None = None,
        subnet_status_code: str | None = None,
        subnet_name: str | None = None,
        subnet: str | None = None,
        subnet_no_list: list[str] | None = None,
        vpc_no: str | None = None,
        zone_code: str | None = None,
        subnet_type_code: str | None = None,
        usage_type_code: str | None = None,
        network_acl_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_subnet_params(
            region_code=region_code,
            subnet_status_code=subnet_status_code,
            subnet_name=subnet_name,
            subnet=subnet,
            subnet_no_list=subnet_no_list,
            vpc_no=vpc_no,
            zone_code=zone_code,
            subnet_type_code=subnet_type_code,
            usage_type_code=usage_type_code,
            network_acl_no=network_acl_no,
            page_no=page_no,
            page_size=page_size,
        )
        raw = self.request("GET", "/getSubnetList", params=params)
        result: dict[str, Any] = raw["getSubnetListResponse"]
        return result

    async def aget_subnet_list(
        self,
        *,
        region_code: str | None = None,
        subnet_status_code: str | None = None,
        subnet_name: str | None = None,
        subnet: str | None = None,
        subnet_no_list: list[str] | None = None,
        vpc_no: str | None = None,
        zone_code: str | None = None,
        subnet_type_code: str | None = None,
        usage_type_code: str | None = None,
        network_acl_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_subnet_params(
            region_code=region_code,
            subnet_status_code=subnet_status_code,
            subnet_name=subnet_name,
            subnet=subnet,
            subnet_no_list=subnet_no_list,
            vpc_no=vpc_no,
            zone_code=zone_code,
            subnet_type_code=subnet_type_code,
            usage_type_code=usage_type_code,
            network_acl_no=network_acl_no,
            page_no=page_no,
            page_size=page_size,
        )
        raw = await self.arequest("GET", "/getSubnetList", params=params)
        result: dict[str, Any] = raw["getSubnetListResponse"]
        return result
