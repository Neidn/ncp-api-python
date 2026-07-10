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


class HadoopApi(NcpHttpAdapter):
    """Cloud Hadoop (vhadoop)."""

    path_prefix: ClassVar[str] = "/vhadoop/v2"

    def create_cloud_hadoop_instance(
        self,
        *,
        region_code: str | None = None,
        vpc_no: str,
        cloud_hadoop_cluster_name: str,
        cloud_hadoop_cluster_type_code: str,
        cloud_hadoop_admin_user_name: str,
        cloud_hadoop_admin_user_password: str,
        bucket_name: str,
        edge_node_subnet_no: str,
        master_node_subnet_no: str,
        master_node_data_storage_size: int,
        worker_node_subnet_no: str,
        worker_node_data_storage_size: int,
        cloud_hadoop_image_product_code: str | None = None,
        cloud_hadoop_add_on_code_list: list[str] | None = None,
        login_key_name: str | None = None,
        edge_node_product_code: str | None = None,
        master_node_product_code: str | None = None,
        master_node_data_storage_type_code: str | None = None,
        worker_node_product_code: str | None = None,
        worker_node_count: int | None = None,
        worker_node_data_storage_type_code: str | None = None,
        use_kdc: bool | None = None,
        kdc_realm: str | None = None,
        kdc_password: str | None = None,
        use_bootstrap_script: bool | None = None,
        bootstrap_script: str | None = None,
        use_data_catalog: bool | None = None,
        engine_version_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            vpcNo=vpc_no,
            cloudHadoopClusterName=cloud_hadoop_cluster_name,
            cloudHadoopClusterTypeCode=cloud_hadoop_cluster_type_code,
            cloudHadoopAdminUserName=cloud_hadoop_admin_user_name,
            cloudHadoopAdminUserPassword=cloud_hadoop_admin_user_password,
            bucketName=bucket_name,
            edgeNodeSubnetNo=edge_node_subnet_no,
            masterNodeSubnetNo=master_node_subnet_no,
            masterNodeDataStorageSize=master_node_data_storage_size,
            workerNodeSubnetNo=worker_node_subnet_no,
            workerNodeDataStorageSize=worker_node_data_storage_size,
            cloudHadoopImageProductCode=cloud_hadoop_image_product_code,
            loginKeyName=login_key_name,
            edgeNodeProductCode=edge_node_product_code,
            masterNodeProductCode=master_node_product_code,
            masterNodeDataStorageTypeCode=master_node_data_storage_type_code,
            workerNodeProductCode=worker_node_product_code,
            workerNodeCount=worker_node_count,
            workerNodeDataStorageTypeCode=worker_node_data_storage_type_code,
            useKdc=use_kdc,
            kdcRealm=kdc_realm,
            kdcPassword=kdc_password,
            useBootstrapScript=use_bootstrap_script,
            bootstrapScript=bootstrap_script,
            useDataCatalog=use_data_catalog,
            engineVersionCode=engine_version_code,
            responseFormatType="json",
        )
        if cloud_hadoop_add_on_code_list:
            data.update(
                _list_params("cloudHadoopAddOnCodeList", cloud_hadoop_add_on_code_list)
            )
        return self.request("POST", "/createCloudHadoopInstance", data=data)

    async def acreate_cloud_hadoop_instance(
        self,
        *,
        region_code: str | None = None,
        vpc_no: str,
        cloud_hadoop_cluster_name: str,
        cloud_hadoop_cluster_type_code: str,
        cloud_hadoop_admin_user_name: str,
        cloud_hadoop_admin_user_password: str,
        bucket_name: str,
        edge_node_subnet_no: str,
        master_node_subnet_no: str,
        master_node_data_storage_size: int,
        worker_node_subnet_no: str,
        worker_node_data_storage_size: int,
        cloud_hadoop_image_product_code: str | None = None,
        cloud_hadoop_add_on_code_list: list[str] | None = None,
        login_key_name: str | None = None,
        edge_node_product_code: str | None = None,
        master_node_product_code: str | None = None,
        master_node_data_storage_type_code: str | None = None,
        worker_node_product_code: str | None = None,
        worker_node_count: int | None = None,
        worker_node_data_storage_type_code: str | None = None,
        use_kdc: bool | None = None,
        kdc_realm: str | None = None,
        kdc_password: str | None = None,
        use_bootstrap_script: bool | None = None,
        bootstrap_script: str | None = None,
        use_data_catalog: bool | None = None,
        engine_version_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            vpcNo=vpc_no,
            cloudHadoopClusterName=cloud_hadoop_cluster_name,
            cloudHadoopClusterTypeCode=cloud_hadoop_cluster_type_code,
            cloudHadoopAdminUserName=cloud_hadoop_admin_user_name,
            cloudHadoopAdminUserPassword=cloud_hadoop_admin_user_password,
            bucketName=bucket_name,
            edgeNodeSubnetNo=edge_node_subnet_no,
            masterNodeSubnetNo=master_node_subnet_no,
            masterNodeDataStorageSize=master_node_data_storage_size,
            workerNodeSubnetNo=worker_node_subnet_no,
            workerNodeDataStorageSize=worker_node_data_storage_size,
            cloudHadoopImageProductCode=cloud_hadoop_image_product_code,
            loginKeyName=login_key_name,
            edgeNodeProductCode=edge_node_product_code,
            masterNodeProductCode=master_node_product_code,
            masterNodeDataStorageTypeCode=master_node_data_storage_type_code,
            workerNodeProductCode=worker_node_product_code,
            workerNodeCount=worker_node_count,
            workerNodeDataStorageTypeCode=worker_node_data_storage_type_code,
            useKdc=use_kdc,
            kdcRealm=kdc_realm,
            kdcPassword=kdc_password,
            useBootstrapScript=use_bootstrap_script,
            bootstrapScript=bootstrap_script,
            useDataCatalog=use_data_catalog,
            engineVersionCode=engine_version_code,
            responseFormatType="json",
        )
        if cloud_hadoop_add_on_code_list:
            data.update(
                _list_params("cloudHadoopAddOnCodeList", cloud_hadoop_add_on_code_list)
            )
        return await self.arequest("POST", "/createCloudHadoopInstance", data=data)

    def delete_cloud_hadoop_instance(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudHadoopInstanceNo=cloud_hadoop_instance_no,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteCloudHadoopInstance", data=data)

    async def adelete_cloud_hadoop_instance(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_instance_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudHadoopInstanceNo=cloud_hadoop_instance_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deleteCloudHadoopInstance", data=data)

    def change_cloud_hadoop_node_count(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_instance_no: str,
        worker_node_count: int,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudHadoopInstanceNo=cloud_hadoop_instance_no,
            workerNodeCount=worker_node_count,
            responseFormatType="json",
        )
        return self.request("POST", "/changeCloudHadoopNodeCount", data=data)

    async def achange_cloud_hadoop_node_count(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_instance_no: str,
        worker_node_count: int,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudHadoopInstanceNo=cloud_hadoop_instance_no,
            workerNodeCount=worker_node_count,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/changeCloudHadoopNodeCount", data=data)

    def change_cloud_hadoop_node_spec(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_instance_no: str,
        worker_node_product_code: str | None = None,
        edge_node_product_code: str | None = None,
        master_node_product_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudHadoopInstanceNo=cloud_hadoop_instance_no,
            workerNodeProductCode=worker_node_product_code,
            edgeNodeProductCode=edge_node_product_code,
            masterNodeProductCode=master_node_product_code,
            responseFormatType="json",
        )
        return self.request("POST", "/changeCloudHadoopNodeSpec", data=data)

    async def achange_cloud_hadoop_node_spec(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_instance_no: str,
        worker_node_product_code: str | None = None,
        edge_node_product_code: str | None = None,
        master_node_product_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            cloudHadoopInstanceNo=cloud_hadoop_instance_no,
            workerNodeProductCode=worker_node_product_code,
            edgeNodeProductCode=edge_node_product_code,
            masterNodeProductCode=master_node_product_code,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/changeCloudHadoopNodeSpec", data=data)

    def backup_cluster_configuration(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(regionCode=region_code, responseFormatType="json")
        return self.request("POST", "/backupClusterConfiguration", data=data)

    async def abackup_cluster_configuration(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(regionCode=region_code, responseFormatType="json")
        return await self.arequest("POST", "/backupClusterConfiguration", data=data)

    def get_cloud_hadoop_instance_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        vpc_no: str | None = None,
        subnet_no: str | None = None,
        cloud_hadoop_cluster_name: str | None = None,
        cloud_hadoop_instance_no_list: list[str] | None = None,
        cloud_hadoop_server_name: str | None = None,
        cloud_hadoop_server_instance_no_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            cloudHadoopClusterName=cloud_hadoop_cluster_name,
            cloudHadoopServerName=cloud_hadoop_server_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if cloud_hadoop_instance_no_list:
            params.update(
                _list_params("cloudHadoopInstanceNoList", cloud_hadoop_instance_no_list)
            )
        if cloud_hadoop_server_instance_no_list:
            params.update(
                _list_params(
                    "cloudHadoopServerInstanceNoList",
                    cloud_hadoop_server_instance_no_list,
                )
            )
        return self.request("GET", "/getCloudHadoopInstanceList", params=params)

    async def aget_cloud_hadoop_instance_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        vpc_no: str | None = None,
        subnet_no: str | None = None,
        cloud_hadoop_cluster_name: str | None = None,
        cloud_hadoop_instance_no_list: list[str] | None = None,
        cloud_hadoop_server_name: str | None = None,
        cloud_hadoop_server_instance_no_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            cloudHadoopClusterName=cloud_hadoop_cluster_name,
            cloudHadoopServerName=cloud_hadoop_server_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if cloud_hadoop_instance_no_list:
            params.update(
                _list_params("cloudHadoopInstanceNoList", cloud_hadoop_instance_no_list)
            )
        if cloud_hadoop_server_instance_no_list:
            params.update(
                _list_params(
                    "cloudHadoopServerInstanceNoList",
                    cloud_hadoop_server_instance_no_list,
                )
            )
        return await self.arequest("GET", "/getCloudHadoopInstanceList", params=params)

    def get_cloud_hadoop_instance_detail(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_instance_no: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudHadoopInstanceNo=cloud_hadoop_instance_no,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudHadoopInstanceDetail", params=params)

    async def aget_cloud_hadoop_instance_detail(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_instance_no: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudHadoopInstanceNo=cloud_hadoop_instance_no,
            responseFormatType="json",
        )
        return await self.arequest(
            "GET", "/getCloudHadoopInstanceDetail", params=params
        )

    def get_cloud_hadoop_image_product_list(
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
        return self.request("GET", "/getCloudHadoopImageProductList", params=params)

    async def aget_cloud_hadoop_image_product_list(
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
            "GET", "/getCloudHadoopImageProductList", params=params
        )

    def get_cloud_hadoop_product_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        cloud_hadoop_image_product_code: str | None = None,
        product_code: str | None = None,
        infra_resource_detail_type_code: str | None = None,
        exclusion_product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            cloudHadoopImageProductCode=cloud_hadoop_image_product_code,
            productCode=product_code,
            infraResourceDetailTypeCode=infra_resource_detail_type_code,
            exclusionProductCode=exclusion_product_code,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudHadoopProductList", params=params)

    async def aget_cloud_hadoop_product_list(
        self,
        *,
        region_code: str | None = None,
        zone_code: str | None = None,
        cloud_hadoop_image_product_code: str | None = None,
        product_code: str | None = None,
        infra_resource_detail_type_code: str | None = None,
        exclusion_product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            zoneCode=zone_code,
            cloudHadoopImageProductCode=cloud_hadoop_image_product_code,
            productCode=product_code,
            infraResourceDetailTypeCode=infra_resource_detail_type_code,
            exclusionProductCode=exclusion_product_code,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getCloudHadoopProductList", params=params)

    def get_cloud_hadoop_cluster_type_list(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_image_product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudHadoopImageProductCode=cloud_hadoop_image_product_code,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudHadoopClusterTypeList", params=params)

    async def aget_cloud_hadoop_cluster_type_list(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_image_product_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudHadoopImageProductCode=cloud_hadoop_image_product_code,
            responseFormatType="json",
        )
        return await self.arequest(
            "GET", "/getCloudHadoopClusterTypeList", params=params
        )

    def get_cloud_hadoop_add_on_list(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_image_product_code: str,
        cloud_hadoop_cluster_type_code: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudHadoopImageProductCode=cloud_hadoop_image_product_code,
            cloudHadoopClusterTypeCode=cloud_hadoop_cluster_type_code,
            responseFormatType="json",
        )
        return self.request("GET", "/getCloudHadoopAddOnList", params=params)

    async def aget_cloud_hadoop_add_on_list(
        self,
        *,
        region_code: str | None = None,
        cloud_hadoop_image_product_code: str,
        cloud_hadoop_cluster_type_code: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            cloudHadoopImageProductCode=cloud_hadoop_image_product_code,
            cloudHadoopClusterTypeCode=cloud_hadoop_cluster_type_code,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getCloudHadoopAddOnList", params=params)

    def get_cloud_hadoop_bucket_list(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(regionCode=region_code, responseFormatType="json")
        return self.request("GET", "/getCloudHadoopBucketList", params=params)

    async def aget_cloud_hadoop_bucket_list(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(regionCode=region_code, responseFormatType="json")
        return await self.arequest("GET", "/getCloudHadoopBucketList", params=params)

    def get_cloud_hadoop_login_key_list(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(regionCode=region_code, responseFormatType="json")
        return self.request("GET", "/getCloudHadoopLoginKeyList", params=params)

    async def aget_cloud_hadoop_login_key_list(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(regionCode=region_code, responseFormatType="json")
        return await self.arequest("GET", "/getCloudHadoopLoginKeyList", params=params)
