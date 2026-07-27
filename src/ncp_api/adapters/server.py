from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


def _list_params(key: str, values: list[str]) -> dict[str, str]:
    return {f"{key}.{i + 1}": v for i, v in enumerate(values)}


class ServerApi(NcpHttpAdapter):
    path_prefix: ClassVar[str] = "/vserver/v2"

    def _get_server_instance_list_params(
        self,
        *,
        region_code: str | None,
        vpc_no: str | None,
        server_instance_no_list: list[str] | None,
        server_name: str | None,
        server_instance_status_code: str | None,
        base_block_storage_disk_type_code: str | None,
        base_block_storage_disk_detail_type_code: str | None,
        ip: str | None,
        placement_group_no_list: list[str] | None,
        hypervisor_type_code_list: list[str] | None,
        fabric_cluster_pool_no: str | None,
        fabric_cluster_no: str | None,
        fabric_cluster_mode: str | None,
        page_no: int | None,
        page_size: int | None,
        sorted_by: str | None,
        sorting_order: str | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            vpcNo=vpc_no,
            serverName=server_name,
            serverInstanceStatusCode=server_instance_status_code,
            baseBlockStorageDiskTypeCode=base_block_storage_disk_type_code,
            baseBlockStorageDiskDetailTypeCode=base_block_storage_disk_detail_type_code,
            ip=ip,
            fabricClusterPoolNo=fabric_cluster_pool_no,
            fabricClusterNo=fabric_cluster_no,
            fabricClusterMode=fabric_cluster_mode,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        if server_instance_no_list:
            params.update(_list_params("serverInstanceNoList", server_instance_no_list))
        if placement_group_no_list:
            params.update(_list_params("placementGroupNoList", placement_group_no_list))
        if hypervisor_type_code_list:
            params.update(
                _list_params("hypervisorTypeCodeList", hypervisor_type_code_list)
            )
        return params

    def get_server_instance_list(
        self,
        *,
        region_code: str | None = None,
        vpc_no: str | None = None,
        server_instance_no_list: list[str] | None = None,
        server_name: str | None = None,
        server_instance_status_code: str | None = None,
        base_block_storage_disk_type_code: str | None = None,
        base_block_storage_disk_detail_type_code: str | None = None,
        ip: str | None = None,
        placement_group_no_list: list[str] | None = None,
        hypervisor_type_code_list: list[str] | None = None,
        fabric_cluster_pool_no: str | None = None,
        fabric_cluster_no: str | None = None,
        fabric_cluster_mode: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_server_instance_list_params(
            region_code=region_code,
            vpc_no=vpc_no,
            server_instance_no_list=server_instance_no_list,
            server_name=server_name,
            server_instance_status_code=server_instance_status_code,
            base_block_storage_disk_type_code=base_block_storage_disk_type_code,
            base_block_storage_disk_detail_type_code=base_block_storage_disk_detail_type_code,
            ip=ip,
            placement_group_no_list=placement_group_no_list,
            hypervisor_type_code_list=hypervisor_type_code_list,
            fabric_cluster_pool_no=fabric_cluster_pool_no,
            fabric_cluster_no=fabric_cluster_no,
            fabric_cluster_mode=fabric_cluster_mode,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = self.request("GET", "/getServerInstanceList", params=params)
        result: dict[str, Any] = raw["getServerInstanceListResponse"]
        return result

    async def aget_server_instance_list(
        self,
        *,
        region_code: str | None = None,
        vpc_no: str | None = None,
        server_instance_no_list: list[str] | None = None,
        server_name: str | None = None,
        server_instance_status_code: str | None = None,
        base_block_storage_disk_type_code: str | None = None,
        base_block_storage_disk_detail_type_code: str | None = None,
        ip: str | None = None,
        placement_group_no_list: list[str] | None = None,
        hypervisor_type_code_list: list[str] | None = None,
        fabric_cluster_pool_no: str | None = None,
        fabric_cluster_no: str | None = None,
        fabric_cluster_mode: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_server_instance_list_params(
            region_code=region_code,
            vpc_no=vpc_no,
            server_instance_no_list=server_instance_no_list,
            server_name=server_name,
            server_instance_status_code=server_instance_status_code,
            base_block_storage_disk_type_code=base_block_storage_disk_type_code,
            base_block_storage_disk_detail_type_code=base_block_storage_disk_detail_type_code,
            ip=ip,
            placement_group_no_list=placement_group_no_list,
            hypervisor_type_code_list=hypervisor_type_code_list,
            fabric_cluster_pool_no=fabric_cluster_pool_no,
            fabric_cluster_no=fabric_cluster_no,
            fabric_cluster_mode=fabric_cluster_mode,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = await self.arequest("GET", "/getServerInstanceList", params=params)
        result: dict[str, Any] = raw["getServerInstanceListResponse"]
        return result

    # --- Public IP ---

    def _get_public_ip_params(
        self,
        *,
        region_code: str | None,
        is_associated: bool | None,
        public_ip_instance_no_list: list[str] | None,
        public_ip: str | None,
        public_ip_kind_type_code: str | None,
        server_instance_no: str | None,
        page_no: int | None,
        page_size: int | None,
        sorted_by: str | None,
        sorting_order: str | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            isAssociated=is_associated,
            publicIp=public_ip,
            publicIpKindTypeCode=public_ip_kind_type_code,
            serverInstanceNo=server_instance_no,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        if public_ip_instance_no_list:
            params.update(
                _list_params("publicIpInstanceNoList", public_ip_instance_no_list)
            )
        return params

    def get_public_ip_instance_list(
        self,
        *,
        region_code: str | None = None,
        is_associated: bool | None = None,
        public_ip_instance_no_list: list[str] | None = None,
        public_ip: str | None = None,
        public_ip_kind_type_code: str | None = None,
        server_instance_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_public_ip_params(
            region_code=region_code,
            is_associated=is_associated,
            public_ip_instance_no_list=public_ip_instance_no_list,
            public_ip=public_ip,
            public_ip_kind_type_code=public_ip_kind_type_code,
            server_instance_no=server_instance_no,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = self.request("GET", "/getPublicIpInstanceList", params=params)
        result: dict[str, Any] = raw["getPublicIpInstanceListResponse"]
        return result

    async def aget_public_ip_instance_list(
        self,
        *,
        region_code: str | None = None,
        is_associated: bool | None = None,
        public_ip_instance_no_list: list[str] | None = None,
        public_ip: str | None = None,
        public_ip_kind_type_code: str | None = None,
        server_instance_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_public_ip_params(
            region_code=region_code,
            is_associated=is_associated,
            public_ip_instance_no_list=public_ip_instance_no_list,
            public_ip=public_ip,
            public_ip_kind_type_code=public_ip_kind_type_code,
            server_instance_no=server_instance_no,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = await self.arequest("GET", "/getPublicIpInstanceList", params=params)
        result: dict[str, Any] = raw["getPublicIpInstanceListResponse"]
        return result

    # --- Network Interface ---

    def _get_network_interface_list_params(
        self,
        *,
        region_code: str | None,
        subnet_name: str | None,
        network_interface_no_list: list[str] | None,
        network_interface_name: str | None,
        network_interface_status_code: str | None,
        ip: str | None,
        secondary_ip_list: list[str] | None,
        instance_no: str | None,
        is_default: bool | None,
        device_name: str | None,
        server_name: str | None,
        page_no: int | None,
        page_size: int | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            subnetName=subnet_name,
            networkInterfaceName=network_interface_name,
            networkInterfaceStatusCode=network_interface_status_code,
            ip=ip,
            instanceNo=instance_no,
            isDefault=is_default,
            deviceName=device_name,
            serverName=server_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if network_interface_no_list:
            params.update(
                _list_params("networkInterfaceNoList", network_interface_no_list)
            )
        if secondary_ip_list:
            params.update(_list_params("secondaryIpList", secondary_ip_list))
        return params

    def get_network_interface_list(
        self,
        *,
        region_code: str | None = None,
        subnet_name: str | None = None,
        network_interface_no_list: list[str] | None = None,
        network_interface_name: str | None = None,
        network_interface_status_code: str | None = None,
        ip: str | None = None,
        secondary_ip_list: list[str] | None = None,
        instance_no: str | None = None,
        is_default: bool | None = None,
        device_name: str | None = None,
        server_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_network_interface_list_params(
            region_code=region_code,
            subnet_name=subnet_name,
            network_interface_no_list=network_interface_no_list,
            network_interface_name=network_interface_name,
            network_interface_status_code=network_interface_status_code,
            ip=ip,
            secondary_ip_list=secondary_ip_list,
            instance_no=instance_no,
            is_default=is_default,
            device_name=device_name,
            server_name=server_name,
            page_no=page_no,
            page_size=page_size,
        )
        raw = self.request("GET", "/getNetworkInterfaceList", params=params)
        result: dict[str, Any] = raw["getNetworkInterfaceListResponse"]
        return result

    async def aget_network_interface_list(
        self,
        *,
        region_code: str | None = None,
        subnet_name: str | None = None,
        network_interface_no_list: list[str] | None = None,
        network_interface_name: str | None = None,
        network_interface_status_code: str | None = None,
        ip: str | None = None,
        secondary_ip_list: list[str] | None = None,
        instance_no: str | None = None,
        is_default: bool | None = None,
        device_name: str | None = None,
        server_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_network_interface_list_params(
            region_code=region_code,
            subnet_name=subnet_name,
            network_interface_no_list=network_interface_no_list,
            network_interface_name=network_interface_name,
            network_interface_status_code=network_interface_status_code,
            ip=ip,
            secondary_ip_list=secondary_ip_list,
            instance_no=instance_no,
            is_default=is_default,
            device_name=device_name,
            server_name=server_name,
            page_no=page_no,
            page_size=page_size,
        )
        raw = await self.arequest("GET", "/getNetworkInterfaceList", params=params)
        result: dict[str, Any] = raw["getNetworkInterfaceListResponse"]
        return result

    # --- Access Control Group ---

    def _get_access_control_group_list_params(
        self,
        *,
        region_code: str | None,
        vpc_no: str | None,
        access_control_group_no_list: list[str] | None,
        access_control_group_name: str | None,
        access_control_group_status_code: str | None,
        page_no: int | None,
        page_size: int | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            vpcNo=vpc_no,
            accessControlGroupName=access_control_group_name,
            accessControlGroupStatusCode=access_control_group_status_code,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if access_control_group_no_list:
            params.update(
                _list_params("accessControlGroupNoList", access_control_group_no_list)
            )
        return params

    def get_access_control_group_list(
        self,
        *,
        region_code: str | None = None,
        vpc_no: str | None = None,
        access_control_group_no_list: list[str] | None = None,
        access_control_group_name: str | None = None,
        access_control_group_status_code: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_access_control_group_list_params(
            region_code=region_code,
            vpc_no=vpc_no,
            access_control_group_no_list=access_control_group_no_list,
            access_control_group_name=access_control_group_name,
            access_control_group_status_code=access_control_group_status_code,
            page_no=page_no,
            page_size=page_size,
        )
        raw = self.request("GET", "/getAccessControlGroupList", params=params)
        result: dict[str, Any] = raw["getAccessControlGroupListResponse"]
        return result

    async def aget_access_control_group_list(
        self,
        *,
        region_code: str | None = None,
        vpc_no: str | None = None,
        access_control_group_no_list: list[str] | None = None,
        access_control_group_name: str | None = None,
        access_control_group_status_code: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_access_control_group_list_params(
            region_code=region_code,
            vpc_no=vpc_no,
            access_control_group_no_list=access_control_group_no_list,
            access_control_group_name=access_control_group_name,
            access_control_group_status_code=access_control_group_status_code,
            page_no=page_no,
            page_size=page_size,
        )
        raw = await self.arequest("GET", "/getAccessControlGroupList", params=params)
        result: dict[str, Any] = raw["getAccessControlGroupListResponse"]
        return result

    def get_access_control_group_rule_list(
        self,
        *,
        access_control_group_no: str,
        region_code: str | None = None,
        access_control_group_rule_type_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            accessControlGroupNo=access_control_group_no,
            accessControlGroupRuleTypeCode=access_control_group_rule_type_code,
            responseFormatType="json",
        )
        raw = self.request("GET", "/getAccessControlGroupRuleList", params=params)
        result: dict[str, Any] = raw["getAccessControlGroupRuleListResponse"]
        return result

    async def aget_access_control_group_rule_list(
        self,
        *,
        access_control_group_no: str,
        region_code: str | None = None,
        access_control_group_rule_type_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            accessControlGroupNo=access_control_group_no,
            accessControlGroupRuleTypeCode=access_control_group_rule_type_code,
            responseFormatType="json",
        )
        raw = await self.arequest(
            "GET", "/getAccessControlGroupRuleList", params=params
        )
        result: dict[str, Any] = raw["getAccessControlGroupRuleListResponse"]
        return result
