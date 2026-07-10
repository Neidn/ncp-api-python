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


class MssqlApi(NcpHttpAdapter):
    """Cloud MSSQL (vmssql)."""

    path_prefix: ClassVar[str] = "/vmssql/v2"

    def create_cloud_mssql_instance(
        self,
        *,
        region_code: str | None = None,
        vpc_no: str,
        subnet_no: str,
        cloud_mssql_service_name: str,
        cloud_mssql_user_name: str,
        cloud_mssql_user_password: str,
        config_group_no: str | None = None,
        cloud_mssql_image_product_code: str | None = None,
        cloud_mssql_product_code: str | None = None,
        data_storage_type_code: str | None = None,
        is_ha: bool | None = None,
        backup_file_retention_period: int | None = None,
        backup_time: str | None = None,
        is_automatic_backup: bool | None = None,
        cloud_mssql_port: int | None = None,
        character_set_name: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            cloudMssqlServiceName=cloud_mssql_service_name,
            cloudMssqlUserName=cloud_mssql_user_name,
            cloudMssqlUserPassword=cloud_mssql_user_password,
            configGroupNo=config_group_no,
            cloudMssqlImageProductCode=cloud_mssql_image_product_code,
            cloudMssqlProductCode=cloud_mssql_product_code,
            dataStorageTypeCode=data_storage_type_code,
            isHa=is_ha,
            backupFileRetentionPeriod=backup_file_retention_period,
            backupTime=backup_time,
            isAutomaticBackup=is_automatic_backup,
            cloudMssqlPort=cloud_mssql_port,
            characterSetName=character_set_name,
            responseFormatType="json",
        )
        return self.request("POST", "/createCloudMssqlInstance", data=data)

    async def acreate_cloud_mssql_instance(
        self,
        *,
        region_code: str | None = None,
        vpc_no: str,
        subnet_no: str,
        cloud_mssql_service_name: str,
        cloud_mssql_user_name: str,
        cloud_mssql_user_password: str,
        config_group_no: str | None = None,
        cloud_mssql_image_product_code: str | None = None,
        cloud_mssql_product_code: str | None = None,
        data_storage_type_code: str | None = None,
        is_ha: bool | None = None,
        backup_file_retention_period: int | None = None,
        backup_time: str | None = None,
        is_automatic_backup: bool | None = None,
        cloud_mssql_port: int | None = None,
        character_set_name: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            cloudMssqlServiceName=cloud_mssql_service_name,
            cloudMssqlUserName=cloud_mssql_user_name,
            cloudMssqlUserPassword=cloud_mssql_user_password,
            configGroupNo=config_group_no,
            cloudMssqlImageProductCode=cloud_mssql_image_product_code,
            cloudMssqlProductCode=cloud_mssql_product_code,
            dataStorageTypeCode=data_storage_type_code,
            isHa=is_ha,
            backupFileRetentionPeriod=backup_file_retention_period,
            backupTime=backup_time,
            isAutomaticBackup=is_automatic_backup,
            cloudMssqlPort=cloud_mssql_port,
            characterSetName=character_set_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/createCloudMssqlInstance", data=data)

    def create_cloud_mssql_slave_instance(
        self,
        *,
        cloud_mssql_instance_no: str,
        private_domain_postfix: str,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            privateDomainPostfix=private_domain_postfix,
            regionCode=region_code,
            responseFormatType="json",
        )
        return self.request("POST", "/createCloudMssqlSlaveInstance", data=data)

    async def acreate_cloud_mssql_slave_instance(
        self,
        *,
        cloud_mssql_instance_no: str,
        private_domain_postfix: str,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            privateDomainPostfix=private_domain_postfix,
            regionCode=region_code,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/createCloudMssqlSlaveInstance", data=data)

    def delete_cloud_mssql_instance(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteCloudMssqlInstance", data=data)

    async def adelete_cloud_mssql_instance(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deleteCloudMssqlInstance", data=data)

    def delete_cloud_mssql_server_instance(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_server_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlServerInstanceNo=cloud_mssql_server_instance_no,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteCloudMssqlServerInstance", data=data)

    async def adelete_cloud_mssql_server_instance(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_server_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlServerInstanceNo=cloud_mssql_server_instance_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deleteCloudMssqlServerInstance", data=data)

    def reboot_cloud_mssql_server_instance(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_server_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlServerInstanceNo=cloud_mssql_server_instance_no,
            responseFormatType="json",
        )
        return self.request("POST", "/rebootCloudMssqlServerInstance", data=data)

    async def areboot_cloud_mssql_server_instance(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_server_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlServerInstanceNo=cloud_mssql_server_instance_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/rebootCloudMssqlServerInstance", data=data)

    def get_cloud_mssql_instance_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        vpc_no: str | None = None,
        subnet_no: str | None = None,
        cloud_mssql_instance_no_list: list[str] | None = None,
        cloud_mssql_service_name: str | None = None,
        cloud_mssql_server_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            cloudMssqlServiceName=cloud_mssql_service_name,
            cloudMssqlServerName=cloud_mssql_server_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if cloud_mssql_instance_no_list:
            params.update(
                _list_params("cloudMssqlInstanceNoList", cloud_mssql_instance_no_list)
            )
        return self.request("GET", "/getCloudMssqlInstanceList", params=params)

    async def aget_cloud_mssql_instance_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        vpc_no: str | None = None,
        subnet_no: str | None = None,
        cloud_mssql_instance_no_list: list[str] | None = None,
        cloud_mssql_service_name: str | None = None,
        cloud_mssql_server_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            cloudMssqlServiceName=cloud_mssql_service_name,
            cloudMssqlServerName=cloud_mssql_server_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if cloud_mssql_instance_no_list:
            params.update(
                _list_params("cloudMssqlInstanceNoList", cloud_mssql_instance_no_list)
            )
        return await self.arequest("GET", "/getCloudMssqlInstanceList", params=params)

    def get_cloud_mssql_instance_detail(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudMssqlInstanceDetail", params=params)

    async def aget_cloud_mssql_instance_detail(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getCloudMssqlInstanceDetail", params=params)

    def get_cloud_mssql_image_product_list(
        self,
        *,
        region_code: str | None = None,
        product_code: str | None = None,
        exclusion_product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            productCode=product_code,
            exclusionProductCode=exclusion_product_code,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudMssqlImageProductList", params=params)

    async def aget_cloud_mssql_image_product_list(
        self,
        *,
        region_code: str | None = None,
        product_code: str | None = None,
        exclusion_product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            productCode=product_code,
            exclusionProductCode=exclusion_product_code,
            responseFormatType="json",
        )
        return await self.arequest(
            "GET", "/getCloudMssqlImageProductList", params=params
        )

    def get_cloud_mssql_product_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        cloud_mssql_image_product_code: str,
        product_code: str | None = None,
        exclusion_product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            cloudMssqlImageProductCode=cloud_mssql_image_product_code,
            productCode=product_code,
            exclusionProductCode=exclusion_product_code,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudMssqlProductList", params=params)

    async def aget_cloud_mssql_product_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        cloud_mssql_image_product_code: str,
        product_code: str | None = None,
        exclusion_product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            cloudMssqlImageProductCode=cloud_mssql_image_product_code,
            productCode=product_code,
            exclusionProductCode=exclusion_product_code,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getCloudMssqlProductList", params=params)

    def get_cloud_mssql_character_set_list(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(regionCode=region_code, responseFormatType="json")
        return self.request("GET", "/getCloudMssqlCharacterSetList", params=params)

    async def aget_cloud_mssql_character_set_list(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(regionCode=region_code, responseFormatType="json")
        return await self.arequest(
            "GET", "/getCloudMssqlCharacterSetList", params=params
        )

    def get_cloud_mssql_config_group_list(
        self,
        *,
        region_code: str | None = None,
        config_group_no: str | None = None,
        config_group_name: str | None = None,
        cloud_mssql_instance_no: str | None = None,
        cloud_mssql_service_name: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            configGroupNo=config_group_no,
            configGroupName=config_group_name,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            cloudMssqlServiceName=cloud_mssql_service_name,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudMssqlConfigGroupList", params=params)

    async def aget_cloud_mssql_config_group_list(
        self,
        *,
        region_code: str | None = None,
        config_group_no: str | None = None,
        config_group_name: str | None = None,
        cloud_mssql_instance_no: str | None = None,
        cloud_mssql_service_name: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            configGroupNo=config_group_no,
            configGroupName=config_group_name,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            cloudMssqlServiceName=cloud_mssql_service_name,
            responseFormatType="json",
        )
        return await self.arequest(
            "GET", "/getCloudMssqlConfigGroupList", params=params
        )

    def get_cloud_mssql_backup_list(
        self,
        *,
        region_code: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudMssqlBackupList", params=params)

    async def aget_cloud_mssql_backup_list(
        self,
        *,
        region_code: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getCloudMssqlBackupList", params=params)

    def get_cloud_mssql_backup_detail_list(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudMssqlBackupDetailList", params=params)

    async def aget_cloud_mssql_backup_detail_list(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return await self.arequest(
            "GET", "/getCloudMssqlBackupDetailList", params=params
        )

    # --- DMS (Data Migration Service) ---

    def get_dms_backup_list(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        database_name: str | None = None,
        backup_type_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            databaseName=database_name,
            backupTypeCode=backup_type_code,
            responseFormatType="json",
        )
        return self.request("GET", "/getDmsBackupList", params=params)

    async def aget_dms_backup_list(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        database_name: str | None = None,
        backup_type_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            databaseName=database_name,
            backupTypeCode=backup_type_code,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getDmsBackupList", params=params)

    def get_dms_object_storage_backup_list(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        folder_name: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            folderName=folder_name,
            responseFormatType="json",
        )
        return self.request("GET", "/getDmsObjectStorageBackupList", params=params)

    async def aget_dms_object_storage_backup_list(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        folder_name: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            folderName=folder_name,
            responseFormatType="json",
        )
        return await self.arequest(
            "GET", "/getDmsObjectStorageBackupList", params=params
        )

    def get_dms_operation(
        self,
        *,
        region_code: str | None = None,
        request_no: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            requestNo=request_no,
            responseFormatType="json",
        )
        return self.request("GET", "/getDmsOperation", params=params)

    async def aget_dms_operation(
        self,
        *,
        region_code: str | None = None,
        request_no: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            requestNo=request_no,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getDmsOperation", params=params)

    def set_dms_object_storage_info(
        self,
        *,
        region_code: str | None = None,
        object_storage_access_key: str,
        object_storage_secret_key: str,
        endpoint: str,
        bucket_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            objectStorageAccessKey=object_storage_access_key,
            objectStorageSecretKey=object_storage_secret_key,
            endpoint=endpoint,
            bucketName=bucket_name,
            responseFormatType="json",
        )
        return self.request("POST", "/setDmsObjectStorageInfo", data=data)

    async def aset_dms_object_storage_info(
        self,
        *,
        region_code: str | None = None,
        object_storage_access_key: str,
        object_storage_secret_key: str,
        endpoint: str,
        bucket_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            objectStorageAccessKey=object_storage_access_key,
            objectStorageSecretKey=object_storage_secret_key,
            endpoint=endpoint,
            bucketName=bucket_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/setDmsObjectStorageInfo", data=data)

    def upload_dms_file(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        file_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            fileName=file_name,
            responseFormatType="json",
        )
        return self.request("POST", "/uploadDmsFile", data=data)

    async def aupload_dms_file(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        file_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            fileName=file_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/uploadDmsFile", data=data)

    def download_dms_file(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        file_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            fileName=file_name,
            responseFormatType="json",
        )
        return self.request("POST", "/downloadDmsFile", data=data)

    async def adownload_dms_file(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        file_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            fileName=file_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/downloadDmsFile", data=data)

    def restore_dms_database(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        file_name: str,
        is_recovery: bool,
        new_database_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            fileName=file_name,
            isRecovery=is_recovery,
            newDatabaseName=new_database_name,
            responseFormatType="json",
        )
        return self.request("POST", "/restoreDmsDatabase", data=data)

    async def arestore_dms_database(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        file_name: str,
        is_recovery: bool,
        new_database_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            fileName=file_name,
            isRecovery=is_recovery,
            newDatabaseName=new_database_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/restoreDmsDatabase", data=data)

    def restore_dms_transaction_log(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        file_name: str,
        is_recovery: bool,
        new_database_name: str,
        stop_time: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            fileName=file_name,
            isRecovery=is_recovery,
            newDatabaseName=new_database_name,
            stopTime=stop_time,
            responseFormatType="json",
        )
        return self.request("POST", "/restoreDmsTransactionLog", data=data)

    async def arestore_dms_transaction_log(
        self,
        *,
        region_code: str | None = None,
        cloud_mssql_instance_no: str,
        file_name: str,
        is_recovery: bool,
        new_database_name: str,
        stop_time: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudMssqlInstanceNo=cloud_mssql_instance_no,
            fileName=file_name,
            isRecovery=is_recovery,
            newDatabaseName=new_database_name,
            stopTime=stop_time,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/restoreDmsTransactionLog", data=data)
