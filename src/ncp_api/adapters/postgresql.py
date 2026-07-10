from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


def _list_params(key: str, values: list[str]) -> dict[str, str]:
    return {f"{key}.{i + 1}": v for i, v in enumerate(values)}


class CloudPostgresqlApi(NcpHttpAdapter):
    path_prefix: ClassVar[str] = "/vpostgresql/v2"

    def _get_params(
        self,
        *,
        region_code: str | None,
        zone_code: str | None,
        vpc_no: str | None,
        subnet_no: str | None,
        cloud_postgresql_service_name: str | None,
        cloud_postgresql_instance_no_list: list[str] | None,
        cloud_postgresql_server_name: str | None,
        cloud_postgresql_server_instance_no_list: list[str] | None,
        page_no: int | None,
        page_size: int | None,
    ) -> dict[str, str]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            cloudPostgresqlServiceName=cloud_postgresql_service_name,
            cloudPostgresqlServerName=cloud_postgresql_server_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if cloud_postgresql_instance_no_list:
            params.update(
                _list_params(
                    "cloudPostgresqlInstanceNoList", cloud_postgresql_instance_no_list
                )
            )
        if cloud_postgresql_server_instance_no_list:
            params.update(
                _list_params(
                    "cloudPostgresqlServerInstanceNoList",
                    cloud_postgresql_server_instance_no_list,
                )
            )
        return params

    def get_cloud_postgresql_instance_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        vpc_no: str | None = None,
        subnet_no: str | None = None,
        cloud_postgresql_service_name: str | None = None,
        cloud_postgresql_instance_no_list: list[str] | None = None,
        cloud_postgresql_server_name: str | None = None,
        cloud_postgresql_server_instance_no_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_params(
            region_code=region_code,
            zone_code=zone_code,
            vpc_no=vpc_no,
            subnet_no=subnet_no,
            cloud_postgresql_service_name=cloud_postgresql_service_name,
            cloud_postgresql_instance_no_list=cloud_postgresql_instance_no_list,
            cloud_postgresql_server_name=cloud_postgresql_server_name,
            cloud_postgresql_server_instance_no_list=cloud_postgresql_server_instance_no_list,
            page_no=page_no,
            page_size=page_size,
        )
        raw = self.request("GET", "/getCloudPostgresqlInstanceList", params=params)
        result: dict[str, Any] = raw["getCloudPostgresqlInstanceListResponse"]
        return result

    async def aget_cloud_postgresql_instance_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        vpc_no: str | None = None,
        subnet_no: str | None = None,
        cloud_postgresql_service_name: str | None = None,
        cloud_postgresql_instance_no_list: list[str] | None = None,
        cloud_postgresql_server_name: str | None = None,
        cloud_postgresql_server_instance_no_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_params(
            region_code=region_code,
            zone_code=zone_code,
            vpc_no=vpc_no,
            subnet_no=subnet_no,
            cloud_postgresql_service_name=cloud_postgresql_service_name,
            cloud_postgresql_instance_no_list=cloud_postgresql_instance_no_list,
            cloud_postgresql_server_name=cloud_postgresql_server_name,
            cloud_postgresql_server_instance_no_list=cloud_postgresql_server_instance_no_list,
            page_no=page_no,
            page_size=page_size,
        )
        raw = await self.arequest(
            "GET", "/getCloudPostgresqlInstanceList", params=params
        )
        result: dict[str, Any] = raw["getCloudPostgresqlInstanceListResponse"]
        return result
