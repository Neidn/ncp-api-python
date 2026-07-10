from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


def _list_params(key: str, values: list[str]) -> dict[str, str]:
    return {f"{key}.{i + 1}": v for i, v in enumerate(values)}


class BlockStorageApi(NcpHttpAdapter):
    path_prefix: ClassVar[str] = "/vserver/v2"

    def _get_params(
        self,
        *,
        region_code: str | None,
        block_storage_instance_no_list: list[str] | None,
        block_storage_name: str | None,
        block_storage_type_code: str | None,
        block_storage_status_code: str | None,
        server_instance_no: str | None,
        block_storage_disk_type_code: str | None,
        block_storage_disk_detail_type_code: str | None,
        page_no: int | None,
        page_size: int | None,
        sorted_by: str | None,
        sorting_order: str | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            blockStorageName=block_storage_name,
            blockStorageTypeCode=block_storage_type_code,
            blockStorageStatusCode=block_storage_status_code,
            serverInstanceNo=server_instance_no,
            blockStorageDiskTypeCode=block_storage_disk_type_code,
            blockStorageDiskDetailTypeCode=block_storage_disk_detail_type_code,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        if block_storage_instance_no_list:
            params.update(
                _list_params(
                    "blockStorageInstanceNoList", block_storage_instance_no_list
                )
            )
        return params

    def get_block_storage_instance_list(
        self,
        *,
        region_code: str | None = None,
        block_storage_instance_no_list: list[str] | None = None,
        block_storage_name: str | None = None,
        block_storage_type_code: str | None = None,
        block_storage_status_code: str | None = None,
        server_instance_no: str | None = None,
        block_storage_disk_type_code: str | None = None,
        block_storage_disk_detail_type_code: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_params(
            region_code=region_code,
            block_storage_instance_no_list=block_storage_instance_no_list,
            block_storage_name=block_storage_name,
            block_storage_type_code=block_storage_type_code,
            block_storage_status_code=block_storage_status_code,
            server_instance_no=server_instance_no,
            block_storage_disk_type_code=block_storage_disk_type_code,
            block_storage_disk_detail_type_code=block_storage_disk_detail_type_code,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = self.request("GET", "/getBlockStorageInstanceList", params=params)
        result: dict[str, Any] = raw["getBlockStorageInstanceListResponse"]
        return result

    async def aget_block_storage_instance_list(
        self,
        *,
        region_code: str | None = None,
        block_storage_instance_no_list: list[str] | None = None,
        block_storage_name: str | None = None,
        block_storage_type_code: str | None = None,
        block_storage_status_code: str | None = None,
        server_instance_no: str | None = None,
        block_storage_disk_type_code: str | None = None,
        block_storage_disk_detail_type_code: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = self._get_params(
            region_code=region_code,
            block_storage_instance_no_list=block_storage_instance_no_list,
            block_storage_name=block_storage_name,
            block_storage_type_code=block_storage_type_code,
            block_storage_status_code=block_storage_status_code,
            server_instance_no=server_instance_no,
            block_storage_disk_type_code=block_storage_disk_type_code,
            block_storage_disk_detail_type_code=block_storage_disk_detail_type_code,
            page_no=page_no,
            page_size=page_size,
            sorted_by=sorted_by,
            sorting_order=sorting_order,
        )
        raw = await self.arequest("GET", "/getBlockStorageInstanceList", params=params)
        result: dict[str, Any] = raw["getBlockStorageInstanceListResponse"]
        return result
