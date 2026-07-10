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


class ClassicAutoScalingApi(NcpHttpAdapter):
    """Classic Auto Scaling (autoscaling). Uses signature v1."""

    path_prefix: ClassVar[str] = "/autoscaling/v2"
    _signature_version: ClassVar[str] = "v1"

    def create_launch_configuration(
        self,
        *,
        region_no: str | None = None,
        launch_configuration_name: str | None = None,
        server_image_product_code: str | None = None,
        server_product_code: str | None = None,
        member_server_image_no: str | None = None,
        login_key_name: str | None = None,
        user_data: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionNo=region_no,
            launchConfigurationName=launch_configuration_name,
            serverImageProductCode=server_image_product_code,
            serverProductCode=server_product_code,
            memberServerImageNo=member_server_image_no,
            loginKeyName=login_key_name,
            userData=user_data,
            responseFormatType="json",
        )
        return self.request("POST", "/createLaunchConfiguration", data=data)

    async def acreate_launch_configuration(
        self,
        *,
        region_no: str | None = None,
        launch_configuration_name: str | None = None,
        server_image_product_code: str | None = None,
        server_product_code: str | None = None,
        member_server_image_no: str | None = None,
        login_key_name: str | None = None,
        user_data: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionNo=region_no,
            launchConfigurationName=launch_configuration_name,
            serverImageProductCode=server_image_product_code,
            serverProductCode=server_product_code,
            memberServerImageNo=member_server_image_no,
            loginKeyName=login_key_name,
            userData=user_data,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/createLaunchConfiguration", data=data)

    def get_launch_configuration_list(
        self,
        *,
        region_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionNo=region_no,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        return self.request("GET", "/getLaunchConfigurationList", params=params)

    async def aget_launch_configuration_list(
        self,
        *,
        region_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionNo=region_no,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getLaunchConfigurationList", params=params)

    def delete_auto_scaling_launch_configuration(
        self,
        *,
        launch_configuration_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            launchConfigurationName=launch_configuration_name,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteAutoScalingLaunchConfiguration", data=data)

    async def adelete_auto_scaling_launch_configuration(
        self,
        *,
        launch_configuration_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            launchConfigurationName=launch_configuration_name,
            responseFormatType="json",
        )
        return await self.arequest(
            "POST", "/deleteAutoScalingLaunchConfiguration", data=data
        )

    def create_auto_scaling_group(
        self,
        *,
        launch_configuration_name: str,
        min_size: int,
        max_size: int,
        region_no: str | None = None,
        auto_scaling_group_name: str | None = None,
        desired_capacity: int | None = None,
        default_cooldown: int | None = None,
        health_check_grace_period: int | None = None,
        health_check_type_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            launchConfigurationName=launch_configuration_name,
            minSize=min_size,
            maxSize=max_size,
            regionNo=region_no,
            autoScalingGroupName=auto_scaling_group_name,
            desiredCapacity=desired_capacity,
            defaultCooldown=default_cooldown,
            healthCheckGracePeriod=health_check_grace_period,
            healthCheckTypeCode=health_check_type_code,
            responseFormatType="json",
        )
        return self.request("POST", "/createAutoScalingGroup", data=data)

    async def acreate_auto_scaling_group(
        self,
        *,
        launch_configuration_name: str,
        min_size: int,
        max_size: int,
        region_no: str | None = None,
        auto_scaling_group_name: str | None = None,
        desired_capacity: int | None = None,
        default_cooldown: int | None = None,
        health_check_grace_period: int | None = None,
        health_check_type_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            launchConfigurationName=launch_configuration_name,
            minSize=min_size,
            maxSize=max_size,
            regionNo=region_no,
            autoScalingGroupName=auto_scaling_group_name,
            desiredCapacity=desired_capacity,
            defaultCooldown=default_cooldown,
            healthCheckGracePeriod=health_check_grace_period,
            healthCheckTypeCode=health_check_type_code,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/createAutoScalingGroup", data=data)

    def get_auto_scaling_group_list(
        self,
        *,
        region_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionNo=region_no,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        return self.request("GET", "/getAutoScalingGroupList", params=params)

    async def aget_auto_scaling_group_list(
        self,
        *,
        region_no: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionNo=region_no,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getAutoScalingGroupList", params=params)

    def update_auto_scaling_group(
        self,
        *,
        launch_configuration_name: str,
        region_no: str | None = None,
        auto_scaling_group_name: str | None = None,
        desired_capacity: int | None = None,
        min_size: int | None = None,
        max_size: int | None = None,
        default_cooldown: int | None = None,
        health_check_grace_period: int | None = None,
        health_check_type_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            launchConfigurationName=launch_configuration_name,
            regionNo=region_no,
            autoScalingGroupName=auto_scaling_group_name,
            desiredCapacity=desired_capacity,
            minSize=min_size,
            maxSize=max_size,
            defaultCooldown=default_cooldown,
            healthCheckGracePeriod=health_check_grace_period,
            healthCheckTypeCode=health_check_type_code,
            responseFormatType="json",
        )
        return self.request("POST", "/updateAutoScalingGroup", data=data)

    async def aupdate_auto_scaling_group(
        self,
        *,
        launch_configuration_name: str,
        region_no: str | None = None,
        auto_scaling_group_name: str | None = None,
        desired_capacity: int | None = None,
        min_size: int | None = None,
        max_size: int | None = None,
        default_cooldown: int | None = None,
        health_check_grace_period: int | None = None,
        health_check_type_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            launchConfigurationName=launch_configuration_name,
            regionNo=region_no,
            autoScalingGroupName=auto_scaling_group_name,
            desiredCapacity=desired_capacity,
            minSize=min_size,
            maxSize=max_size,
            defaultCooldown=default_cooldown,
            healthCheckGracePeriod=health_check_grace_period,
            healthCheckTypeCode=health_check_type_code,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/updateAutoScalingGroup", data=data)

    def delete_auto_scaling_group(
        self,
        *,
        auto_scaling_group_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteAutoScalingGroup", data=data)

    async def adelete_auto_scaling_group(
        self,
        *,
        auto_scaling_group_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deleteAutoScalingGroup", data=data)

    def set_desired_capacity(
        self,
        *,
        auto_scaling_group_name: str,
        desired_capacity: int,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            desiredCapacity=desired_capacity,
            responseFormatType="json",
        )
        return self.request("POST", "/setDesiredCapacity", data=data)

    async def aset_desired_capacity(
        self,
        *,
        auto_scaling_group_name: str,
        desired_capacity: int,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            desiredCapacity=desired_capacity,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/setDesiredCapacity", data=data)

    def set_server_instance_health(
        self,
        *,
        health_status_code: str,
        server_instance_no: str,
        should_respect_grace_period: bool | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            healthStatusCode=health_status_code,
            serverInstanceNo=server_instance_no,
            shouldRespectGracePeriod=should_respect_grace_period,
            responseFormatType="json",
        )
        return self.request("POST", "/setServerInstanceHealth", data=data)

    async def aset_server_instance_health(
        self,
        *,
        health_status_code: str,
        server_instance_no: str,
        should_respect_grace_period: bool | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            healthStatusCode=health_status_code,
            serverInstanceNo=server_instance_no,
            shouldRespectGracePeriod=should_respect_grace_period,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/setServerInstanceHealth", data=data)

    def resume_processes(
        self,
        *,
        auto_scaling_group_name: str,
        scaling_process_code_list: list[str] | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            responseFormatType="json",
        )
        if scaling_process_code_list:
            data.update(
                _list_params("scalingProcessCodeList", scaling_process_code_list)
            )
        return self.request("POST", "/resumeProcesses", data=data)

    async def aresume_processes(
        self,
        *,
        auto_scaling_group_name: str,
        scaling_process_code_list: list[str] | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            responseFormatType="json",
        )
        if scaling_process_code_list:
            data.update(
                _list_params("scalingProcessCodeList", scaling_process_code_list)
            )
        return await self.arequest("POST", "/resumeProcesses", data=data)

    def suspend_processes(
        self,
        *,
        auto_scaling_group_name: str,
        scaling_process_code_list: list[str] | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            responseFormatType="json",
        )
        if scaling_process_code_list:
            data.update(
                _list_params("scalingProcessCodeList", scaling_process_code_list)
            )
        return self.request("POST", "/suspendProcesses", data=data)

    async def asuspend_processes(
        self,
        *,
        auto_scaling_group_name: str,
        scaling_process_code_list: list[str] | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            responseFormatType="json",
        )
        if scaling_process_code_list:
            data.update(
                _list_params("scalingProcessCodeList", scaling_process_code_list)
            )
        return await self.arequest("POST", "/suspendProcesses", data=data)

    def get_scaling_process_type_list(self) -> dict[str, Any]:
        params = _build_params(responseFormatType="json")
        return self.request("GET", "/getScalingProcessTypeList", params=params)

    async def aget_scaling_process_type_list(self) -> dict[str, Any]:
        params = _build_params(responseFormatType="json")
        return await self.arequest("GET", "/getScalingProcessTypeList", params=params)

    def put_scaling_policy(
        self,
        *,
        auto_scaling_group_name: str,
        policy_name: str,
        adjustment_type_code: str,
        scaling_adjustment: int,
        cooldown: int | None = None,
        min_adjustment_step: int | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            policyName=policy_name,
            adjustmentTypeCode=adjustment_type_code,
            scalingAdjustment=scaling_adjustment,
            cooldown=cooldown,
            minAdjustmentStep=min_adjustment_step,
            responseFormatType="json",
        )
        return self.request("POST", "/putScalingPolicy", data=data)

    async def aput_scaling_policy(
        self,
        *,
        auto_scaling_group_name: str,
        policy_name: str,
        adjustment_type_code: str,
        scaling_adjustment: int,
        cooldown: int | None = None,
        min_adjustment_step: int | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            policyName=policy_name,
            adjustmentTypeCode=adjustment_type_code,
            scalingAdjustment=scaling_adjustment,
            cooldown=cooldown,
            minAdjustmentStep=min_adjustment_step,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/putScalingPolicy", data=data)

    def get_auto_scaling_policy_list(
        self,
        *,
        auto_scaling_group_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return self.request("GET", "/getAutoScalingPolicyList", params=params)

    async def aget_auto_scaling_policy_list(
        self,
        *,
        auto_scaling_group_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getAutoScalingPolicyList", params=params)

    def delete_policy(
        self,
        *,
        auto_scaling_group_name: str,
        policy_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            policyName=policy_name,
            responseFormatType="json",
        )
        return self.request("POST", "/deletePolicy", data=data)

    async def adelete_policy(
        self,
        *,
        auto_scaling_group_name: str,
        policy_name: str,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            policyName=policy_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deletePolicy", data=data)

    def execute_policy(
        self,
        *,
        auto_scaling_group_name: str,
        policy_name: str,
        honor_cooldown: bool | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            policyName=policy_name,
            honorCooldown=honor_cooldown,
            responseFormatType="json",
        )
        return self.request("POST", "/executePolicy", data=data)

    async def aexecute_policy(
        self,
        *,
        auto_scaling_group_name: str,
        policy_name: str,
        honor_cooldown: bool | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            policyName=policy_name,
            honorCooldown=honor_cooldown,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/executePolicy", data=data)

    def get_adjustment_type_list(self) -> dict[str, Any]:
        params = _build_params(responseFormatType="json")
        return self.request("GET", "/getAdjustmentTypeList", params=params)

    async def aget_adjustment_type_list(self) -> dict[str, Any]:
        params = _build_params(responseFormatType="json")
        return await self.arequest("GET", "/getAdjustmentTypeList", params=params)

    def put_scheduled_update_group_action(
        self,
        *,
        auto_scaling_group_name: str,
        scheduled_action_name: str,
        min_size: int | None = None,
        max_size: int | None = None,
        desired_capacity: int | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        recurrence_in_kst: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            scheduledActionName=scheduled_action_name,
            minSize=min_size,
            maxSize=max_size,
            desiredCapacity=desired_capacity,
            startTime=start_time,
            endTime=end_time,
            recurrenceInKST=recurrence_in_kst,
            responseFormatType="json",
        )
        return self.request("POST", "/putScheduledUpdateGroupAction", data=data)

    async def aput_scheduled_update_group_action(
        self,
        *,
        auto_scaling_group_name: str,
        scheduled_action_name: str,
        min_size: int | None = None,
        max_size: int | None = None,
        desired_capacity: int | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        recurrence_in_kst: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            scheduledActionName=scheduled_action_name,
            minSize=min_size,
            maxSize=max_size,
            desiredCapacity=desired_capacity,
            startTime=start_time,
            endTime=end_time,
            recurrenceInKST=recurrence_in_kst,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/putScheduledUpdateGroupAction", data=data)

    def get_scheduled_action_list(
        self,
        *,
        auto_scaling_group_name: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            startTime=start_time,
            endTime=end_time,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        return self.request("GET", "/getScheduledActionList", params=params)

    async def aget_scheduled_action_list(
        self,
        *,
        auto_scaling_group_name: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            startTime=start_time,
            endTime=end_time,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getScheduledActionList", params=params)

    def delete_scheduled_action(
        self,
        *,
        scheduled_action_name: str,
        auto_scaling_group_name: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            scheduledActionName=scheduled_action_name,
            autoScalingGroupName=auto_scaling_group_name,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteScheduledAction", data=data)

    async def adelete_scheduled_action(
        self,
        *,
        scheduled_action_name: str,
        auto_scaling_group_name: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            scheduledActionName=scheduled_action_name,
            autoScalingGroupName=auto_scaling_group_name,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deleteScheduledAction", data=data)

    def get_auto_scaling_activity_log_list(
        self,
        *,
        auto_scaling_group_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return self.request("GET", "/getAutoScalingActivityLogList", params=params)

    async def aget_auto_scaling_activity_log_list(
        self,
        *,
        auto_scaling_group_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return await self.arequest(
            "GET", "/getAutoScalingActivityLogList", params=params
        )

    def get_auto_scaling_configuration_log_list(
        self,
        *,
        auto_scaling_group_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return self.request("GET", "/getAutoScalingConfigurationLogList", params=params)

    async def aget_auto_scaling_configuration_log_list(
        self,
        *,
        auto_scaling_group_name: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            autoScalingGroupName=auto_scaling_group_name,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        return await self.arequest(
            "GET", "/getAutoScalingConfigurationLogList", params=params
        )
