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

    # --- NAT Gateway ---

    def _get_nat_gateway_params(
        self,
        *,
        region_code: str | None,
        nat_gateway_instance_no_list: list[str] | None,
        nat_gateway_name: str | None,
        nat_gateway_status_code: str | None,
        vpc_no: str | None,
        subnet_no: str | None,
        page_no: int | None,
        page_size: int | None,
        sorted_by: str | None,
        sorting_order: str | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            natGatewayName=nat_gateway_name,
            natGatewayStatusCode=nat_gateway_status_code,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        if nat_gateway_instance_no_list:
            params.update(
                _list_params("natGatewayInstanceNoList", nat_gateway_instance_no_list)
            )
        return params

    def get_nat_gateway_instance_list(
        self,
        *,
        region_code: str | None = None,
        nat_gateway_instance_no_list: list[str] | None = None,
        nat_gateway_name: str | None = None,
        nat_gateway_status_code: str | None = None,
        vpc_no: str | None = None,
        subnet_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_nat_gateway_params(
            region_code=region_code,
            nat_gateway_instance_no_list=nat_gateway_instance_no_list,
            nat_gateway_name=nat_gateway_name,
            nat_gateway_status_code=nat_gateway_status_code,
            vpc_no=vpc_no,
            subnet_no=subnet_no,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = self.request("GET", "/getNatGatewayInstanceList", params=params)
        result: dict[str, Any] = raw["getNatGatewayInstanceListResponse"]
        return result

    async def aget_nat_gateway_instance_list(
        self,
        *,
        region_code: str | None = None,
        nat_gateway_instance_no_list: list[str] | None = None,
        nat_gateway_name: str | None = None,
        nat_gateway_status_code: str | None = None,
        vpc_no: str | None = None,
        subnet_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_nat_gateway_params(
            region_code=region_code,
            nat_gateway_instance_no_list=nat_gateway_instance_no_list,
            nat_gateway_name=nat_gateway_name,
            nat_gateway_status_code=nat_gateway_status_code,
            vpc_no=vpc_no,
            subnet_no=subnet_no,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = await self.arequest("GET", "/getNatGatewayInstanceList", params=params)
        result: dict[str, Any] = raw["getNatGatewayInstanceListResponse"]
        return result

    # --- VPC Peering ---

    def _get_vpc_peering_params(
        self,
        *,
        region_code: str | None,
        vpc_peering_instance_no_list: list[str] | None,
        vpc_peering_name: str | None,
        vpc_peering_status_code: str | None,
        source_vpc_no: str | None,
        target_vpc_no: str | None,
        page_no: int | None,
        page_size: int | None,
        sorted_by: str | None,
        sorting_order: str | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            vpcPeeringName=vpc_peering_name,
            vpcPeeringStatusCode=vpc_peering_status_code,
            sourceVpcNo=source_vpc_no,
            targetVpcNo=target_vpc_no,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        if vpc_peering_instance_no_list:
            params.update(
                _list_params("vpcPeeringInstanceNoList", vpc_peering_instance_no_list)
            )
        return params

    def get_vpc_peering_instance_list(
        self,
        *,
        region_code: str | None = None,
        vpc_peering_instance_no_list: list[str] | None = None,
        vpc_peering_name: str | None = None,
        vpc_peering_status_code: str | None = None,
        source_vpc_no: str | None = None,
        target_vpc_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_vpc_peering_params(
            region_code=region_code,
            vpc_peering_instance_no_list=vpc_peering_instance_no_list,
            vpc_peering_name=vpc_peering_name,
            vpc_peering_status_code=vpc_peering_status_code,
            source_vpc_no=source_vpc_no,
            target_vpc_no=target_vpc_no,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = self.request("GET", "/getVpcPeeringInstanceList", params=params)
        result: dict[str, Any] = raw["getVpcPeeringInstanceListResponse"]
        return result

    async def aget_vpc_peering_instance_list(
        self,
        *,
        region_code: str | None = None,
        vpc_peering_instance_no_list: list[str] | None = None,
        vpc_peering_name: str | None = None,
        vpc_peering_status_code: str | None = None,
        source_vpc_no: str | None = None,
        target_vpc_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_vpc_peering_params(
            region_code=region_code,
            vpc_peering_instance_no_list=vpc_peering_instance_no_list,
            vpc_peering_name=vpc_peering_name,
            vpc_peering_status_code=vpc_peering_status_code,
            source_vpc_no=source_vpc_no,
            target_vpc_no=target_vpc_no,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = await self.arequest("GET", "/getVpcPeeringInstanceList", params=params)
        result: dict[str, Any] = raw["getVpcPeeringInstanceListResponse"]
        return result

    # --- Route Table ---

    def _get_route_table_params(
        self,
        *,
        region_code: str | None,
        route_table_no_list: list[str] | None,
        route_table_name: str | None,
        route_table_status_code: str | None,
        route_table_type_code: str | None,
        vpc_no: str | None,
        supported_subnet_type_code: str | None,
        page_no: int | None,
        page_size: int | None,
        sorted_by: str | None,
        sorting_order: str | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            routeTableName=route_table_name,
            routeTableStatusCode=route_table_status_code,
            routeTableTypeCode=route_table_type_code,
            vpcNo=vpc_no,
            supportedSubnetTypeCode=supported_subnet_type_code,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        if route_table_no_list:
            params.update(_list_params("routeTableNoList", route_table_no_list))
        return params

    def get_route_table_list(
        self,
        *,
        region_code: str | None = None,
        route_table_no_list: list[str] | None = None,
        route_table_name: str | None = None,
        route_table_status_code: str | None = None,
        route_table_type_code: str | None = None,
        vpc_no: str | None = None,
        supported_subnet_type_code: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_route_table_params(
            region_code=region_code,
            route_table_no_list=route_table_no_list,
            route_table_name=route_table_name,
            route_table_status_code=route_table_status_code,
            route_table_type_code=route_table_type_code,
            vpc_no=vpc_no,
            supported_subnet_type_code=supported_subnet_type_code,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = self.request("GET", "/getRouteTableList", params=params)
        result: dict[str, Any] = raw["getRouteTableListResponse"]
        return result

    async def aget_route_table_list(
        self,
        *,
        region_code: str | None = None,
        route_table_no_list: list[str] | None = None,
        route_table_name: str | None = None,
        route_table_status_code: str | None = None,
        route_table_type_code: str | None = None,
        vpc_no: str | None = None,
        supported_subnet_type_code: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_route_table_params(
            region_code=region_code,
            route_table_no_list=route_table_no_list,
            route_table_name=route_table_name,
            route_table_status_code=route_table_status_code,
            route_table_type_code=route_table_type_code,
            vpc_no=vpc_no,
            supported_subnet_type_code=supported_subnet_type_code,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = await self.arequest("GET", "/getRouteTableList", params=params)
        result: dict[str, Any] = raw["getRouteTableListResponse"]
        return result

    # --- Route Table Subnet ---

    def _get_route_table_subnet_params(
        self,
        *,
        region_code: str | None,
        route_table_no: str,
        subnet_no_list: list[str] | None,
        page_no: int | None,
        page_size: int | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            routeTableNo=route_table_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if subnet_no_list:
            params.update(_list_params("subnetNoList", subnet_no_list))
        return params

    def get_route_table_subnet_list(
        self,
        route_table_no: str,
        *,
        region_code: str | None = None,
        subnet_no_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_route_table_subnet_params(
            region_code=region_code,
            route_table_no=route_table_no,
            subnet_no_list=subnet_no_list,
            page_no=page_no,
            page_size=page_size,
        )
        raw = self.request("GET", "/getRouteTableSubnetList", params=params)
        result: dict[str, Any] = raw["getRouteTableSubnetListResponse"]
        return result

    async def aget_route_table_subnet_list(
        self,
        route_table_no: str,
        *,
        region_code: str | None = None,
        subnet_no_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_route_table_subnet_params(
            region_code=region_code,
            route_table_no=route_table_no,
            subnet_no_list=subnet_no_list,
            page_no=page_no,
            page_size=page_size,
        )
        raw = await self.arequest("GET", "/getRouteTableSubnetList", params=params)
        result: dict[str, Any] = raw["getRouteTableSubnetListResponse"]
        return result

    # --- Route ---

    def _get_route_params(
        self,
        *,
        region_code: str | None,
        route_table_no: str,
        vpc_no: str,
    ) -> dict[str, str]:
        return _build_params(
            regionCode=region_code,
            routeTableNo=route_table_no,
            vpcNo=vpc_no,
            responseFormatType="json",
        )

    def get_route_list(
        self,
        route_table_no: str,
        vpc_no: str,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_route_params(
            region_code=region_code,
            route_table_no=route_table_no,
            vpc_no=vpc_no,
        )
        raw = self.request("GET", "/getRouteList", params=params)
        result: dict[str, Any] = raw["getRouteListResponse"]
        return result

    async def aget_route_list(
        self,
        route_table_no: str,
        vpc_no: str,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_route_params(
            region_code=region_code,
            route_table_no=route_table_no,
            vpc_no=vpc_no,
        )
        raw = await self.arequest("GET", "/getRouteList", params=params)
        result: dict[str, Any] = raw["getRouteListResponse"]
        return result

    # --- Network ACL ---

    def _get_network_acl_list_params(
        self,
        *,
        region_code: str | None,
        network_acl_name: str | None,
        network_acl_status_code: str | None,
        network_acl_no_list: list[str] | None,
        page_no: int | None,
        page_size: int | None,
        vpc_no: str | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            networkAclName=network_acl_name,
            networkAclStatusCode=network_acl_status_code,
            pageNo=page_no,
            pageSize=page_size,
            vpcNo=vpc_no,
            responseFormatType="json",
        )
        if network_acl_no_list:
            params.update(_list_params("networkAclNoList", network_acl_no_list))
        return params

    def get_network_acl_list(
        self,
        *,
        region_code: str | None = None,
        network_acl_name: str | None = None,
        network_acl_status_code: str | None = None,
        network_acl_no_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        vpc_no: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_network_acl_list_params(
            region_code=region_code,
            network_acl_name=network_acl_name,
            network_acl_status_code=network_acl_status_code,
            network_acl_no_list=network_acl_no_list,
            page_no=page_no,
            page_size=page_size,
            vpc_no=vpc_no,
        )
        raw = self.request("GET", "/getNetworkAclList", params=params)
        result: dict[str, Any] = raw["getNetworkAclListResponse"]
        return result

    async def aget_network_acl_list(
        self,
        *,
        region_code: str | None = None,
        network_acl_name: str | None = None,
        network_acl_status_code: str | None = None,
        network_acl_no_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        vpc_no: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_network_acl_list_params(
            region_code=region_code,
            network_acl_name=network_acl_name,
            network_acl_status_code=network_acl_status_code,
            network_acl_no_list=network_acl_no_list,
            page_no=page_no,
            page_size=page_size,
            vpc_no=vpc_no,
        )
        raw = await self.arequest("GET", "/getNetworkAclList", params=params)
        result: dict[str, Any] = raw["getNetworkAclListResponse"]
        return result

    def get_network_acl_detail(
        self,
        *,
        network_acl_no: str,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            networkAclNo=network_acl_no,
            responseFormatType="json",
        )
        raw = self.request("GET", "/getNetworkAclDetail", params=params)
        result: dict[str, Any] = raw["getNetworkAclDetailResponse"]
        return result

    async def aget_network_acl_detail(
        self,
        *,
        network_acl_no: str,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            networkAclNo=network_acl_no,
            responseFormatType="json",
        )
        raw = await self.arequest("GET", "/getNetworkAclDetail", params=params)
        result: dict[str, Any] = raw["getNetworkAclDetailResponse"]
        return result

    def get_network_acl_rule_list(
        self,
        *,
        network_acl_no: str,
        region_code: str | None = None,
        network_acl_rule_type_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            networkAclNo=network_acl_no,
            networkAclRuleTypeCode=network_acl_rule_type_code,
            responseFormatType="json",
        )
        raw = self.request("GET", "/getNetworkAclRuleList", params=params)
        result: dict[str, Any] = raw["getNetworkAclRuleListResponse"]
        return result

    async def aget_network_acl_rule_list(
        self,
        *,
        network_acl_no: str,
        region_code: str | None = None,
        network_acl_rule_type_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            networkAclNo=network_acl_no,
            networkAclRuleTypeCode=network_acl_rule_type_code,
            responseFormatType="json",
        )
        raw = await self.arequest("GET", "/getNetworkAclRuleList", params=params)
        result: dict[str, Any] = raw["getNetworkAclRuleListResponse"]
        return result

    # --- Network ACL Deny-Allow Group ---

    def _get_network_acl_deny_allow_group_list_params(
        self,
        *,
        region_code: str | None,
        vpc_no: str | None,
        network_acl_deny_allow_group_name: str | None,
        network_acl_deny_allow_group_status_code: str | None,
        network_acl_deny_allow_group_no_list: list[str] | None,
        is_applied: bool | None,
        page_no: int | None,
        page_size: int | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            vpcNo=vpc_no,
            networkAclDenyAllowGroupName=network_acl_deny_allow_group_name,
            networkAclDenyAllowGroupStatusCode=network_acl_deny_allow_group_status_code,
            isApplied=(str(is_applied).lower() if is_applied is not None else None),
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if network_acl_deny_allow_group_no_list:
            params.update(
                _list_params(
                    "networkAclDenyAllowGroupNoList",
                    network_acl_deny_allow_group_no_list,
                )
            )
        return params

    def get_network_acl_deny_allow_group_list(
        self,
        *,
        region_code: str | None = None,
        vpc_no: str | None = None,
        network_acl_deny_allow_group_name: str | None = None,
        network_acl_deny_allow_group_status_code: str | None = None,
        network_acl_deny_allow_group_no_list: list[str] | None = None,
        is_applied: bool | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_network_acl_deny_allow_group_list_params(
            region_code=region_code,
            vpc_no=vpc_no,
            network_acl_deny_allow_group_name=network_acl_deny_allow_group_name,
            network_acl_deny_allow_group_status_code=(
                network_acl_deny_allow_group_status_code
            ),
            network_acl_deny_allow_group_no_list=network_acl_deny_allow_group_no_list,
            is_applied=is_applied,
            page_no=page_no,
            page_size=page_size,
        )
        raw = self.request("GET", "/getNetworkAclDenyAllowGroupList", params=params)
        result: dict[str, Any] = raw["getNetworkAclDenyAllowGroupListResponse"]
        return result

    async def aget_network_acl_deny_allow_group_list(
        self,
        *,
        region_code: str | None = None,
        vpc_no: str | None = None,
        network_acl_deny_allow_group_name: str | None = None,
        network_acl_deny_allow_group_status_code: str | None = None,
        network_acl_deny_allow_group_no_list: list[str] | None = None,
        is_applied: bool | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_network_acl_deny_allow_group_list_params(
            region_code=region_code,
            vpc_no=vpc_no,
            network_acl_deny_allow_group_name=network_acl_deny_allow_group_name,
            network_acl_deny_allow_group_status_code=(
                network_acl_deny_allow_group_status_code
            ),
            network_acl_deny_allow_group_no_list=network_acl_deny_allow_group_no_list,
            is_applied=is_applied,
            page_no=page_no,
            page_size=page_size,
        )
        raw = await self.arequest(
            "GET", "/getNetworkAclDenyAllowGroupList", params=params
        )
        result: dict[str, Any] = raw["getNetworkAclDenyAllowGroupListResponse"]
        return result

    def get_network_acl_deny_allow_group_detail(
        self,
        *,
        network_acl_deny_allow_group_no: str,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            networkAclDenyAllowGroupNo=network_acl_deny_allow_group_no,
            responseFormatType="json",
        )
        raw = self.request("GET", "/getNetworkAclDenyAllowGroupDetail", params=params)
        result: dict[str, Any] = raw["getNetworkAclDenyAllowGroupDetailResponse"]
        return result

    async def aget_network_acl_deny_allow_group_detail(
        self,
        *,
        network_acl_deny_allow_group_no: str,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            networkAclDenyAllowGroupNo=network_acl_deny_allow_group_no,
            responseFormatType="json",
        )
        raw = await self.arequest(
            "GET", "/getNetworkAclDenyAllowGroupDetail", params=params
        )
        result: dict[str, Any] = raw["getNetworkAclDenyAllowGroupDetailResponse"]
        return result
