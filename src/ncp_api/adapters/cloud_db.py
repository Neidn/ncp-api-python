from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter


def _build_params(**kwargs: Any) -> dict[str, str]:
    result: dict[str, str] = {}
    for k, v in kwargs.items():
        if v is not None:
            result[k] = "true" if v is True else ("false" if v is False else str(v))
    return result


class CloudDbApi(NcpHttpAdapter):
    """Classic Cloud DB (clouddb). Uses signature v1."""

    path_prefix: ClassVar[str] = "/clouddb/v2"
    _signature_version: ClassVar[str] = "v1"

    def create_cloud_db_instance(
        self,
        *,
        db_kind_code: str,
        cloud_db_service_name: str,
        region_no: str | None = None,
        zone_no: str | None = None,
        cloud_db_image_product_code: str | None = None,
        cloud_db_product_code: str | None = None,
        collation: str | None = None,
        data_storage_type_code: str | None = None,
        is_ha: bool | None = None,
        host_ip: str | None = None,
        cloud_db_server_name: str | None = None,
        cloud_db_basic_name: str | None = None,
        cloud_db_user_name: str | None = None,
        cloud_db_user_password: str | None = None,
        cloud_db_port: int | None = None,
        cloud_db_config_group_no: str | None = None,
        is_backup: bool | None = None,
        backup_file_retention_period: int | None = None,
        is_automatic_backup: bool | None = None,
        backup_time: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            dbKindCode=db_kind_code,
            cloudDBServiceName=cloud_db_service_name,
            regionNo=region_no,
            zoneNo=zone_no,
            cloudDBImageProductCode=cloud_db_image_product_code,
            cloudDBProductCode=cloud_db_product_code,
            collation=collation,
            dataStorageTypeCode=data_storage_type_code,
            isHa=is_ha,
            hostIp=host_ip,
            cloudDBServerName=cloud_db_server_name,
            cloudDBBasicName=cloud_db_basic_name,
            cloudDBUserName=cloud_db_user_name,
            cloudDBUserPassword=cloud_db_user_password,
            cloudDBPort=cloud_db_port,
            cloudDBConfigGroupNo=cloud_db_config_group_no,
            isBackup=is_backup,
            backupFileRetentionPeriod=backup_file_retention_period,
            isAutomaticBackup=is_automatic_backup,
            backupTime=backup_time,
            responseFormatType="json",
        )
        return self.request("POST", "/createCloudDBInstance", data=data)

    async def acreate_cloud_db_instance(
        self,
        *,
        db_kind_code: str,
        cloud_db_service_name: str,
        region_no: str | None = None,
        zone_no: str | None = None,
        cloud_db_image_product_code: str | None = None,
        cloud_db_product_code: str | None = None,
        collation: str | None = None,
        data_storage_type_code: str | None = None,
        is_ha: bool | None = None,
        host_ip: str | None = None,
        cloud_db_server_name: str | None = None,
        cloud_db_basic_name: str | None = None,
        cloud_db_user_name: str | None = None,
        cloud_db_user_password: str | None = None,
        cloud_db_port: int | None = None,
        cloud_db_config_group_no: str | None = None,
        is_backup: bool | None = None,
        backup_file_retention_period: int | None = None,
        is_automatic_backup: bool | None = None,
        backup_time: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            dbKindCode=db_kind_code,
            cloudDBServiceName=cloud_db_service_name,
            regionNo=region_no,
            zoneNo=zone_no,
            cloudDBImageProductCode=cloud_db_image_product_code,
            cloudDBProductCode=cloud_db_product_code,
            collation=collation,
            dataStorageTypeCode=data_storage_type_code,
            isHa=is_ha,
            hostIp=host_ip,
            cloudDBServerName=cloud_db_server_name,
            cloudDBBasicName=cloud_db_basic_name,
            cloudDBUserName=cloud_db_user_name,
            cloudDBUserPassword=cloud_db_user_password,
            cloudDBPort=cloud_db_port,
            cloudDBConfigGroupNo=cloud_db_config_group_no,
            isBackup=is_backup,
            backupFileRetentionPeriod=backup_file_retention_period,
            isAutomaticBackup=is_automatic_backup,
            backupTime=backup_time,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/createCloudDBInstance", data=data)

    def get_cloud_db_instance_list(
        self,
        *,
        db_kind_code: str,
        region_no: str | None = None,
        zone_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        search_filter_name: str | None = None,
        search_filter_value: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            dbKindCode=db_kind_code,
            regionNo=region_no,
            zoneNo=zone_no,
            pageNo=page_no,
            pageSize=page_size,
            searchFilterName=search_filter_name,
            searchFilterValue=search_filter_value,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudDBInstanceList", params=params)

    async def aget_cloud_db_instance_list(
        self,
        *,
        db_kind_code: str,
        region_no: str | None = None,
        zone_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        search_filter_name: str | None = None,
        search_filter_value: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            dbKindCode=db_kind_code,
            regionNo=region_no,
            zoneNo=zone_no,
            pageNo=page_no,
            pageSize=page_size,
            searchFilterName=search_filter_name,
            searchFilterValue=search_filter_value,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getCloudDBInstanceList", params=params)

    def delete_cloud_db_server_instance(
        self,
        *,
        cloud_db_server_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBServerInstanceNo=cloud_db_server_instance_no,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteCloudDBServerInstance", data=data)

    async def adelete_cloud_db_server_instance(
        self,
        *,
        cloud_db_server_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBServerInstanceNo=cloud_db_server_instance_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deleteCloudDBServerInstance", data=data)

    def reboot_cloud_db_server_instance(
        self,
        *,
        cloud_db_server_instance_no: str,
        is_with_failover: bool | None = None,
        is_reboot_now: bool | None = None,
        reboot_time: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBServerInstanceNo=cloud_db_server_instance_no,
            isWithFailover=is_with_failover,
            isRebootNow=is_reboot_now,
            rebootTime=reboot_time,
            responseFormatType="json",
        )
        return self.request("POST", "/rebootCloudDBServerInstance", data=data)

    async def areboot_cloud_db_server_instance(
        self,
        *,
        cloud_db_server_instance_no: str,
        is_with_failover: bool | None = None,
        is_reboot_now: bool | None = None,
        reboot_time: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBServerInstanceNo=cloud_db_server_instance_no,
            isWithFailover=is_with_failover,
            isRebootNow=is_reboot_now,
            rebootTime=reboot_time,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/rebootCloudDBServerInstance", data=data)

    def flush_cloud_db_instance(
        self,
        *,
        cloud_db_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            responseFormatType="json",
        )
        return self.request("POST", "/flushCloudDBInstance", data=data)

    async def aflush_cloud_db_instance(
        self,
        *,
        cloud_db_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/flushCloudDBInstance", data=data)

    def get_cloud_db_image_product_list(
        self,
        *,
        region_no: str | None = None,
        db_kind_code: str | None = None,
        exclusion_product_code: str | None = None,
        product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionNo=region_no,
            dbKindCode=db_kind_code,
            exclusionProductCode=exclusion_product_code,
            productCode=product_code,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudDBImageProductList", params=params)

    async def aget_cloud_db_image_product_list(
        self,
        *,
        region_no: str | None = None,
        db_kind_code: str | None = None,
        exclusion_product_code: str | None = None,
        product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionNo=region_no,
            dbKindCode=db_kind_code,
            exclusionProductCode=exclusion_product_code,
            productCode=product_code,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getCloudDBImageProductList", params=params)

    def get_cloud_db_product_list(
        self,
        *,
        cloud_db_image_product_code: str,
        region_no: str | None = None,
        zone_no: str | None = None,
        exclusion_product_code: str | None = None,
        product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            cloudDBImageProductCode=cloud_db_image_product_code,
            regionNo=region_no,
            zoneNo=zone_no,
            exclusionProductCode=exclusion_product_code,
            productCode=product_code,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudDBProductList", params=params)

    async def aget_cloud_db_product_list(
        self,
        *,
        cloud_db_image_product_code: str,
        region_no: str | None = None,
        zone_no: str | None = None,
        exclusion_product_code: str | None = None,
        product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            cloudDBImageProductCode=cloud_db_image_product_code,
            regionNo=region_no,
            zoneNo=zone_no,
            exclusionProductCode=exclusion_product_code,
            productCode=product_code,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getCloudDBProductList", params=params)

    def get_cloud_db_config_group_list(
        self,
        *,
        db_kind_code: str,
    ) -> dict[str, Any]:
        params = _build_params(dbKindCode=db_kind_code, responseFormatType="json")
        return self.request("GET", "/getCloudDBConfigGroupList", params=params)

    async def aget_cloud_db_config_group_list(
        self,
        *,
        db_kind_code: str,
    ) -> dict[str, Any]:
        params = _build_params(dbKindCode=db_kind_code, responseFormatType="json")
        return await self.arequest("GET", "/getCloudDBConfigGroupList", params=params)

    def get_backup_list(
        self,
        *,
        cloud_db_instance_no: str,
        database_name: str | None = None,
        backup_type_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            databaseName=database_name,
            backupTypeCode=backup_type_code,
            responseFormatType="json",
        )
        return self.request("GET", "/getBackupList", params=params)

    async def aget_backup_list(
        self,
        *,
        cloud_db_instance_no: str,
        database_name: str | None = None,
        backup_type_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            databaseName=database_name,
            backupTypeCode=backup_type_code,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getBackupList", params=params)

    def get_object_storage_backup_list(
        self,
        *,
        cloud_db_instance_no: str,
        folder_name: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            folderName=folder_name,
            responseFormatType="json",
        )
        return self.request("GET", "/getObjectStorageBackupList", params=params)

    async def aget_object_storage_backup_list(
        self,
        *,
        cloud_db_instance_no: str,
        folder_name: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            folderName=folder_name,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getObjectStorageBackupList", params=params)

    def set_object_storage_info(
        self,
        *,
        object_storage_access_key: str,
        object_storage_secret_key: str,
        endpoint: str,
        bucket_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            objectStorageAccessKey=object_storage_access_key,
            objectStorageSecretKey=object_storage_secret_key,
            endpoint=endpoint,
            bucketName=bucket_name,
            responseFormatType="json",
        )
        return self.request("POST", "/setObjectStorageInfo", data=data)

    async def aset_object_storage_info(
        self,
        *,
        object_storage_access_key: str,
        object_storage_secret_key: str,
        endpoint: str,
        bucket_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            objectStorageAccessKey=object_storage_access_key,
            objectStorageSecretKey=object_storage_secret_key,
            endpoint=endpoint,
            bucketName=bucket_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/setObjectStorageInfo", data=data)

    def upload_dms_file(
        self,
        *,
        cloud_db_instance_no: str,
        file_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            fileName=file_name,
            responseFormatType="json",
        )
        return self.request("POST", "/uploadDmsFile", data=data)

    async def aupload_dms_file(
        self,
        *,
        cloud_db_instance_no: str,
        file_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            fileName=file_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/uploadDmsFile", data=data)

    def download_dms_file(
        self,
        *,
        cloud_db_instance_no: str,
        file_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            fileName=file_name,
            responseFormatType="json",
        )
        return self.request("POST", "/downloadDmsFile", data=data)

    async def adownload_dms_file(
        self,
        *,
        cloud_db_instance_no: str,
        file_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            fileName=file_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/downloadDmsFile", data=data)

    def get_dms_operation(
        self,
        *,
        request_no: str,
    ) -> dict[str, Any]:
        params = _build_params(requestNo=request_no, responseFormatType="json")
        return self.request("GET", "/getDmsOperation", params=params)

    async def aget_dms_operation(
        self,
        *,
        request_no: str,
    ) -> dict[str, Any]:
        params = _build_params(requestNo=request_no, responseFormatType="json")
        return await self.arequest("GET", "/getDmsOperation", params=params)

    def restore_dms_database(
        self,
        *,
        cloud_db_instance_no: str,
        file_name: str,
        is_recovery: bool,
        new_database_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            fileName=file_name,
            isRecovery=is_recovery,
            newDatabaseName=new_database_name,
            responseFormatType="json",
        )
        return self.request("POST", "/restoreDmsDatabase", data=data)

    async def arestore_dms_database(
        self,
        *,
        cloud_db_instance_no: str,
        file_name: str,
        is_recovery: bool,
        new_database_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            fileName=file_name,
            isRecovery=is_recovery,
            newDatabaseName=new_database_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/restoreDmsDatabase", data=data)

    def restore_dms_transaction_log(
        self,
        *,
        cloud_db_instance_no: str,
        file_name: str,
        is_recovery: bool,
        new_database_name: str,
        stop_time: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
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
        cloud_db_instance_no: str,
        file_name: str,
        is_recovery: bool,
        new_database_name: str,
        stop_time: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            cloudDBInstanceNo=cloud_db_instance_no,
            fileName=file_name,
            isRecovery=is_recovery,
            newDatabaseName=new_database_name,
            stopTime=stop_time,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/restoreDmsTransactionLog", data=data)
