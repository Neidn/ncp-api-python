from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


def _list_params(key: str, values: list[str]) -> dict[str, str]:
    return {f"{key}.{i + 1}": v for i, v in enumerate(values)}


class NasApi(NcpHttpAdapter):
    path_prefix: ClassVar[str] = "/vnas/v2"

    def _get_params(
        self,
        *,
        region_code: str | None,
        zone_code: str | None,
        nas_volume_instance_no_list: list[str] | None,
        volume_name: str | None,
        volume_allotment_protocol_type_code: str | None,
        is_event_configuration: bool | None,
        is_snapshot_configuration: bool | None,
        page_no: int | None,
        page_size: int | None,
        sorted_by: str | None,
        sorting_order: str | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            volumeName=volume_name,
            volumeAllotmentProtocolTypeCode=volume_allotment_protocol_type_code,
            isEventConfiguration=is_event_configuration,
            isSnapshotConfiguration=is_snapshot_configuration,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        if nas_volume_instance_no_list:
            params.update(_list_params("nasVolumeInstanceNoList", nas_volume_instance_no_list))
        return params

    def get_nas_volume_instance_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        nas_volume_instance_no_list: list[str] | None = None,
        volume_name: str | None = None,
        volume_allotment_protocol_type_code: str | None = None,
        is_event_configuration: bool | None = None,
        is_snapshot_configuration: bool | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_params(
            region_code=region_code,
            zone_code=zone_code,
            nas_volume_instance_no_list=nas_volume_instance_no_list,
            volume_name=volume_name,
            volume_allotment_protocol_type_code=volume_allotment_protocol_type_code,
            is_event_configuration=is_event_configuration,
            is_snapshot_configuration=is_snapshot_configuration,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = self.request("GET", "/getNasVolumeInstanceList", params=params)
        result: dict[str, Any] = raw["getNasVolumeInstanceListResponse"]
        return result

    async def aget_nas_volume_instance_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        nas_volume_instance_no_list: list[str] | None = None,
        volume_name: str | None = None,
        volume_allotment_protocol_type_code: str | None = None,
        is_event_configuration: bool | None = None,
        is_snapshot_configuration: bool | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_params(
            region_code=region_code,
            zone_code=zone_code,
            nas_volume_instance_no_list=nas_volume_instance_no_list,
            volume_name=volume_name,
            volume_allotment_protocol_type_code=volume_allotment_protocol_type_code,
            is_event_configuration=is_event_configuration,
            is_snapshot_configuration=is_snapshot_configuration,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = await self.arequest("GET", "/getNasVolumeInstanceList", params=params)
        result: dict[str, Any] = raw["getNasVolumeInstanceListResponse"]
        return result
