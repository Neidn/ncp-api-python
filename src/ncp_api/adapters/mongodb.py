from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


def _list_params(key: str, values: list[str]) -> dict[str, str]:
    return {f"{key}.{i + 1}": v for i, v in enumerate(values)}


class CloudMongoDbApi(NcpHttpAdapter):
    path_prefix: ClassVar[str] = "/vmongodb/v2"

    def _get_cloud_mongodb_instance_list_params(
        self,
        *,
        region_code: str | None,
        zone_code: str | None,
        vpc_no: str | None,
        subnet_no: str | None,
        cloud_mongodb_service_name: str | None,
        cloud_mongodb_instance_no_list: list[str] | None,
        cloud_mongodb_server_name: str | None,
        cloud_mongodb_server_instance_no_list: list[str] | None,
        generation_code: str | None,
        page_no: int | None,
        page_size: int | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            cloudMongoDbServiceName=cloud_mongodb_service_name,
            cloudMongoDbServerName=cloud_mongodb_server_name,
            generationCode=generation_code,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if cloud_mongodb_instance_no_list:
            params.update(
                _list_params(
                    "cloudMongoDbInstanceNoList", cloud_mongodb_instance_no_list
                )
            )
        if cloud_mongodb_server_instance_no_list:
            params.update(
                _list_params(
                    "cloudMongoDbServerInstanceNoList",
                    cloud_mongodb_server_instance_no_list,
                )
            )
        return params

    def get_cloud_mongodb_instance_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        vpc_no: str | None = None,
        subnet_no: str | None = None,
        cloud_mongodb_service_name: str | None = None,
        cloud_mongodb_instance_no_list: list[str] | None = None,
        cloud_mongodb_server_name: str | None = None,
        cloud_mongodb_server_instance_no_list: list[str] | None = None,
        generation_code: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_cloud_mongodb_instance_list_params(
            region_code=region_code,
            zone_code=zone_code,
            vpc_no=vpc_no,
            subnet_no=subnet_no,
            cloud_mongodb_service_name=cloud_mongodb_service_name,
            cloud_mongodb_instance_no_list=cloud_mongodb_instance_no_list,
            cloud_mongodb_server_name=cloud_mongodb_server_name,
            cloud_mongodb_server_instance_no_list=cloud_mongodb_server_instance_no_list,
            generation_code=generation_code,
            page_no=page_no,
            page_size=page_size,
        )
        raw = self.request("GET", "/getCloudMongoDbInstanceList", params=params)
        result: dict[str, Any] = raw["getCloudMongoDbInstanceListResponse"]
        return result

    async def aget_cloud_mongodb_instance_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        vpc_no: str | None = None,
        subnet_no: str | None = None,
        cloud_mongodb_service_name: str | None = None,
        cloud_mongodb_instance_no_list: list[str] | None = None,
        cloud_mongodb_server_name: str | None = None,
        cloud_mongodb_server_instance_no_list: list[str] | None = None,
        generation_code: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_cloud_mongodb_instance_list_params(
            region_code=region_code,
            zone_code=zone_code,
            vpc_no=vpc_no,
            subnet_no=subnet_no,
            cloud_mongodb_service_name=cloud_mongodb_service_name,
            cloud_mongodb_instance_no_list=cloud_mongodb_instance_no_list,
            cloud_mongodb_server_name=cloud_mongodb_server_name,
            cloud_mongodb_server_instance_no_list=cloud_mongodb_server_instance_no_list,
            generation_code=generation_code,
            page_no=page_no,
            page_size=page_size,
        )
        raw = await self.arequest("GET", "/getCloudMongoDbInstanceList", params=params)
        result: dict[str, Any] = raw["getCloudMongoDbInstanceListResponse"]
        return result
