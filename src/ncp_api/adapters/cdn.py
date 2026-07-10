from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter


def _build_params(**kwargs: Any) -> dict[str, str]:
    result: dict[str, str] = {}
    for k, v in kwargs.items():
        if v is not None:
            result[k] = "true" if v is True else ("false" if v is False else str(v))
    return result


def _list_params(key: str, values: list[str]) -> dict[str, str]:
    return {f"{key}.{i + 1}": v for i, v in enumerate(values)}


class CdnApi(NcpHttpAdapter):
    """CDN (cdn)."""

    path_prefix: ClassVar[str] = "/cdn/v2"

    def get_cdn_plus_instance_list(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return self.request("GET", "/getCdnPlusInstanceList", params=params)

    async def aget_cdn_plus_instance_list(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getCdnPlusInstanceList", params=params)

    def get_cdn_plus_purge_history_list(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str,
        purge_id_list: list[str] | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            responseFormatType="json",
        )
        if purge_id_list:
            params.update(_list_params("purgeIdList", purge_id_list))
        return self.request("GET", "/getCdnPlusPurgeHistoryList", params=params)

    async def aget_cdn_plus_purge_history_list(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str,
        purge_id_list: list[str] | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            responseFormatType="json",
        )
        if purge_id_list:
            params.update(_list_params("purgeIdList", purge_id_list))
        return await self.arequest("GET", "/getCdnPlusPurgeHistoryList", params=params)

    def request_cdn_plus_purge(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str,
        is_whole_purge: bool,
        is_whole_domain: bool,
        domain_id_list: list[str] | None = None,
        target_file_list: list[str] | None = None,
        target_directory_name: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            isWholePurge=is_whole_purge,
            isWholeDomain=is_whole_domain,
            targetDirectoryName=target_directory_name,
            responseFormatType="json",
        )
        if domain_id_list:
            data.update(_list_params("domainIdList", domain_id_list))
        if target_file_list:
            data.update(_list_params("targetFileList", target_file_list))
        return self.request("POST", "/requestCdnPlusPurge", data=data)

    async def arequest_cdn_plus_purge(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str,
        is_whole_purge: bool,
        is_whole_domain: bool,
        domain_id_list: list[str] | None = None,
        target_file_list: list[str] | None = None,
        target_directory_name: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            isWholePurge=is_whole_purge,
            isWholeDomain=is_whole_domain,
            targetDirectoryName=target_directory_name,
            responseFormatType="json",
        )
        if domain_id_list:
            data.update(_list_params("domainIdList", domain_id_list))
        if target_file_list:
            data.update(_list_params("targetFileList", target_file_list))
        return await self.arequest("POST", "/requestCdnPlusPurge", data=data)

    def get_global_cdn_instance_list(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return self.request("GET", "/getGlobalCdnInstanceList", params=params)

    async def aget_global_cdn_instance_list(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getGlobalCdnInstanceList", params=params)

    def get_global_cdn_purge_history_list(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str,
        purge_id_list: list[str] | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            responseFormatType="json",
        )
        if purge_id_list:
            params.update(_list_params("purgeIdList", purge_id_list))
        return self.request("GET", "/getGlobalCdnPurgeHistoryList", params=params)

    async def aget_global_cdn_purge_history_list(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str,
        purge_id_list: list[str] | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            responseFormatType="json",
        )
        if purge_id_list:
            params.update(_list_params("purgeIdList", purge_id_list))
        return await self.arequest(
            "GET", "/getGlobalCdnPurgeHistoryList", params=params
        )

    def request_global_cdn_purge(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str,
        is_whole_purge: bool,
        is_whole_domain: bool,
        service_domain_name_list: list[str] | None = None,
        target_file_list: list[str] | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            isWholePurge=is_whole_purge,
            isWholeDomain=is_whole_domain,
            responseFormatType="json",
        )
        if service_domain_name_list:
            data.update(_list_params("serviceDomainNameList", service_domain_name_list))
        if target_file_list:
            data.update(_list_params("targetFileList", target_file_list))
        return self.request("POST", "/requestGlobalCdnPurge", data=data)

    async def arequest_global_cdn_purge(
        self,
        *,
        region_code: str | None = None,
        cdn_instance_no: str,
        is_whole_purge: bool,
        is_whole_domain: bool,
        service_domain_name_list: list[str] | None = None,
        target_file_list: list[str] | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cdnInstanceNo=cdn_instance_no,
            isWholePurge=is_whole_purge,
            isWholeDomain=is_whole_domain,
            responseFormatType="json",
        )
        if service_domain_name_list:
            data.update(_list_params("serviceDomainNameList", service_domain_name_list))
        if target_file_list:
            data.update(_list_params("targetFileList", target_file_list))
        return await self.arequest("POST", "/requestGlobalCdnPurge", data=data)
