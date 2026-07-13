from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


def _list_params(key: str, values: list[str]) -> dict[str, str]:
    return {f"{key}.{i + 1}": v for i, v in enumerate(values)}


class LoadBalancerApi(NcpHttpAdapter):
    path_prefix: ClassVar[str] = "/vloadbalancer/v2"

    def _get_params(
        self,
        *,
        region_code: str | None,
        load_balancer_instance_no_list: list[str] | None,
        load_balancer_name: str | None,
        load_balancer_network_type_code: str | None,
        load_balancer_type_code: str | None,
        load_balancer_status_code: str | None,
        vpc_no: str | None,
        page_no: int | None,
        page_size: int | None,
        sorted_by: str | None,
        sorting_order: str | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            loadBalancerName=load_balancer_name,
            loadBalancerNetworkTypeCode=load_balancer_network_type_code,
            loadBalancerTypeCode=load_balancer_type_code,
            loadBalancerStatusCode=load_balancer_status_code,
            vpcNo=vpc_no,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        if load_balancer_instance_no_list:
            params.update(
                _list_params(
                    "loadBalancerInstanceNoList", load_balancer_instance_no_list
                )
            )
        return params

    def get_load_balancer_instance_list(
        self,
        *,
        region_code: str | None = None,
        load_balancer_instance_no_list: list[str] | None = None,
        load_balancer_name: str | None = None,
        load_balancer_network_type_code: str | None = None,
        load_balancer_type_code: str | None = None,
        load_balancer_status_code: str | None = None,
        vpc_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_params(
            region_code=region_code,
            load_balancer_instance_no_list=load_balancer_instance_no_list,
            load_balancer_name=load_balancer_name,
            load_balancer_network_type_code=load_balancer_network_type_code,
            load_balancer_type_code=load_balancer_type_code,
            load_balancer_status_code=load_balancer_status_code,
            vpc_no=vpc_no,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = self.request("GET", "/getLoadBalancerInstanceList", params=params)
        result: dict[str, Any] = raw["getLoadBalancerInstanceListResponse"]
        return result

    async def aget_load_balancer_instance_list(
        self,
        *,
        region_code: str | None = None,
        load_balancer_instance_no_list: list[str] | None = None,
        load_balancer_name: str | None = None,
        load_balancer_network_type_code: str | None = None,
        load_balancer_type_code: str | None = None,
        load_balancer_status_code: str | None = None,
        vpc_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_params(
            region_code=region_code,
            load_balancer_instance_no_list=load_balancer_instance_no_list,
            load_balancer_name=load_balancer_name,
            load_balancer_network_type_code=load_balancer_network_type_code,
            load_balancer_type_code=load_balancer_type_code,
            load_balancer_status_code=load_balancer_status_code,
            vpc_no=vpc_no,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = await self.arequest("GET", "/getLoadBalancerInstanceList", params=params)
        result: dict[str, Any] = raw["getLoadBalancerInstanceListResponse"]
        return result

    def _get_target_group_list_params(
        self,
        *,
        region_code: str | None,
        target_group_no_list: list[str] | None,
        target_type_code: str | None,
        vpc_no: str | None,
        page_no: int | None,
        page_size: int | None,
        sorted_by: str | None,
        sorting_order: str | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            targetTypeCode=target_type_code,
            vpcNo=vpc_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if target_group_no_list:
            params.update(_list_params("targetGroupNoList", target_group_no_list))
        if sorted_by is not None:
            params["sortList.1.sortedBy"] = sorted_by
        if sorting_order is not None:
            params["sortList.1.sortingOrder"] = sorting_order
        return params

    def get_target_group_list(
        self,
        *,
        region_code: str | None = None,
        target_group_no_list: list[str] | None = None,
        target_type_code: str | None = None,
        vpc_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_target_group_list_params(
            region_code=region_code,
            target_group_no_list=target_group_no_list,
            target_type_code=target_type_code,
            vpc_no=vpc_no,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = self.request("GET", "/getTargetGroupList", params=params)
        result: dict[str, Any] = raw["getTargetGroupListResponse"]
        return result

    async def aget_target_group_list(
        self,
        *,
        region_code: str | None = None,
        target_group_no_list: list[str] | None = None,
        target_type_code: str | None = None,
        vpc_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_target_group_list_params(
            region_code=region_code,
            target_group_no_list=target_group_no_list,
            target_type_code=target_type_code,
            vpc_no=vpc_no,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = await self.arequest("GET", "/getTargetGroupList", params=params)
        result: dict[str, Any] = raw["getTargetGroupListResponse"]
        return result

    def get_target_group_detail(
        self,
        *,
        target_group_no: str,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            targetGroupNo=target_group_no,
            responseFormatType="json",
        )
        raw = self.request("GET", "/getTargetGroupDetail", params=params)
        result: dict[str, Any] = raw["getTargetGroupDetailResponse"]
        return result

    async def aget_target_group_detail(
        self,
        *,
        target_group_no: str,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            targetGroupNo=target_group_no,
            responseFormatType="json",
        )
        raw = await self.arequest("GET", "/getTargetGroupDetail", params=params)
        result: dict[str, Any] = raw["getTargetGroupDetailResponse"]
        return result
