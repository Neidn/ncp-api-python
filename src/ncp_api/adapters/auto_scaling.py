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


class AutoScalingApi(NcpHttpAdapter):
    """VPC Auto Scaling (vautoscaling)."""

    path_prefix: ClassVar[str] = "/vautoscaling/v2"

    # --- Launch Configuration ---

    def create_launch_configuration(
        self,
        *,
        region_code: str | None = None,
        server_image_product_code: str | None = None,
        member_server_image_instance_no: str | None = None,
        server_product_code: str | None = None,
        is_encrypted_volume: bool | None = None,
        init_script_no: str | None = None,
        launch_configuration_name: str | None = None,
        login_key_name: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            serverImageProductCode=server_image_product_code,
            memberServerImageInstanceNo=member_server_image_instance_no,
            serverProductCode=server_product_code,
            isEncryptedVolume=is_encrypted_volume,
            initScriptNo=init_script_no,
            launchConfigurationName=launch_configuration_name,
            loginKeyName=login_key_name,
            responseFormatType="json",
        )
        return self.request("POST", "/createLaunchConfiguration", data=data)

    async def acreate_launch_configuration(self, **kwargs: Any) -> dict[str, Any]:
        return await self.arequest(
            "POST", "/createLaunchConfiguration", data=self._lc_create_data(**kwargs)
        )

    def _lc_create_data(self, **kwargs: Any) -> dict[str, str]:
        return _build_params(responseFormatType="json", **kwargs)

    def delete_launch_configuration(
        self,
        *,
        region_code: str | None = None,
        launch_configuration_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            launchConfigurationNo=launch_configuration_no,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteLaunchConfiguration", data=data)

    async def adelete_launch_configuration(
        self,
        *,
        region_code: str | None = None,
        launch_configuration_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            launchConfigurationNo=launch_configuration_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deleteLaunchConfiguration", data=data)

    def get_launch_configuration_list(
        self,
        *,
        region_code: str | None = None,
        launch_configuration_no_list: list[str] | None = None,
        launch_configuration_name_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if launch_configuration_no_list:
            params.update(
                _list_params("launchConfigurationNoList", launch_configuration_no_list)
            )
        if launch_configuration_name_list:
            params.update(
                _list_params(
                    "launchConfigurationNameList", launch_configuration_name_list
                )
            )
        return self.request("GET", "/getLaunchConfigurationList", params=params)

    async def aget_launch_configuration_list(
        self,
        *,
        region_code: str | None = None,
        launch_configuration_no_list: list[str] | None = None,
        launch_configuration_name_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if launch_configuration_no_list:
            params.update(
                _list_params("launchConfigurationNoList", launch_configuration_no_list)
            )
        if launch_configuration_name_list:
            params.update(
                _list_params(
                    "launchConfigurationNameList", launch_configuration_name_list
                )
            )
        return await self.arequest("GET", "/getLaunchConfigurationList", params=params)

    def get_launch_configuration_detail(
        self,
        *,
        region_code: str | None = None,
        launch_configuration_no: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            launchConfigurationNo=launch_configuration_no,
            responseFormatType="json",
        )
        return self.request("GET", "/getLaunchConfigurationDetail", params=params)

    async def aget_launch_configuration_detail(
        self,
        *,
        region_code: str | None = None,
        launch_configuration_no: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            launchConfigurationNo=launch_configuration_no,
            responseFormatType="json",
        )
        return await self.arequest(
            "GET", "/getLaunchConfigurationDetail", params=params
        )

    # --- Auto Scaling Group ---

    def create_auto_scaling_group(
        self,
        *,
        region_code: str | None = None,
        launch_configuration_no: str,
        vpc_no: str,
        subnet_no: str,
        access_control_group_no_list: list[str],
        min_size: int,
        max_size: int,
        auto_scaling_group_name: str | None = None,
        server_name_prefix: str | None = None,
        desired_capacity: int | None = None,
        default_cool_down: int | None = None,
        health_check_grace_period: int | None = None,
        health_check_type_code: str | None = None,
        target_group_no_list: list[str] | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            launchConfigurationNo=launch_configuration_no,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            minSize=min_size,
            maxSize=max_size,
            autoScalingGroupName=auto_scaling_group_name,
            serverNamePrefix=server_name_prefix,
            desiredCapacity=desired_capacity,
            defaultCoolDown=default_cool_down,
            healthCheckGracePeriod=health_check_grace_period,
            healthCheckTypeCode=health_check_type_code,
            responseFormatType="json",
        )
        data.update(
            _list_params("accessControlGroupNoList", access_control_group_no_list)
        )
        if target_group_no_list:
            data.update(_list_params("targetGroupNoList", target_group_no_list))
        return self.request("POST", "/createAutoScalingGroup", data=data)

    async def acreate_auto_scaling_group(
        self,
        *,
        region_code: str | None = None,
        launch_configuration_no: str,
        vpc_no: str,
        subnet_no: str,
        access_control_group_no_list: list[str],
        min_size: int,
        max_size: int,
        auto_scaling_group_name: str | None = None,
        server_name_prefix: str | None = None,
        desired_capacity: int | None = None,
        default_cool_down: int | None = None,
        health_check_grace_period: int | None = None,
        health_check_type_code: str | None = None,
        target_group_no_list: list[str] | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            launchConfigurationNo=launch_configuration_no,
            vpcNo=vpc_no,
            subnetNo=subnet_no,
            minSize=min_size,
            maxSize=max_size,
            autoScalingGroupName=auto_scaling_group_name,
            serverNamePrefix=server_name_prefix,
            desiredCapacity=desired_capacity,
            defaultCoolDown=default_cool_down,
            healthCheckGracePeriod=health_check_grace_period,
            healthCheckTypeCode=health_check_type_code,
            responseFormatType="json",
        )
        data.update(
            _list_params("accessControlGroupNoList", access_control_group_no_list)
        )
        if target_group_no_list:
            data.update(_list_params("targetGroupNoList", target_group_no_list))
        return await self.arequest("POST", "/createAutoScalingGroup", data=data)

    def update_auto_scaling_group(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        launch_configuration_no: str | None = None,
        server_name_prefix: str | None = None,
        min_size: int | None = None,
        max_size: int | None = None,
        desired_capacity: int | None = None,
        default_cool_down: int | None = None,
        health_check_grace_period: int | None = None,
        health_check_type_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            launchConfigurationNo=launch_configuration_no,
            serverNamePrefix=server_name_prefix,
            minSize=min_size,
            maxSize=max_size,
            desiredCapacity=desired_capacity,
            defaultCoolDown=default_cool_down,
            healthCheckGracePeriod=health_check_grace_period,
            healthCheckTypeCode=health_check_type_code,
            responseFormatType="json",
        )
        return self.request("POST", "/updateAutoScalingGroup", data=data)

    async def aupdate_auto_scaling_group(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        launch_configuration_no: str | None = None,
        server_name_prefix: str | None = None,
        min_size: int | None = None,
        max_size: int | None = None,
        desired_capacity: int | None = None,
        default_cool_down: int | None = None,
        health_check_grace_period: int | None = None,
        health_check_type_code: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            launchConfigurationNo=launch_configuration_no,
            serverNamePrefix=server_name_prefix,
            minSize=min_size,
            maxSize=max_size,
            desiredCapacity=desired_capacity,
            defaultCoolDown=default_cool_down,
            healthCheckGracePeriod=health_check_grace_period,
            healthCheckTypeCode=health_check_type_code,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/updateAutoScalingGroup", data=data)

    def delete_auto_scaling_group(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteAutoScalingGroup", data=data)

    async def adelete_auto_scaling_group(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deleteAutoScalingGroup", data=data)

    def get_auto_scaling_group_list(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no_list: list[str] | None = None,
        auto_scaling_group_name_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if auto_scaling_group_no_list:
            params.update(
                _list_params("autoScalingGroupNoList", auto_scaling_group_no_list)
            )
        if auto_scaling_group_name_list:
            params.update(
                _list_params("autoScalingGroupNameList", auto_scaling_group_name_list)
            )
        return self.request("GET", "/getAutoScalingGroupList", params=params)

    async def aget_auto_scaling_group_list(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no_list: list[str] | None = None,
        auto_scaling_group_name_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if auto_scaling_group_no_list:
            params.update(
                _list_params("autoScalingGroupNoList", auto_scaling_group_no_list)
            )
        if auto_scaling_group_name_list:
            params.update(
                _list_params("autoScalingGroupNameList", auto_scaling_group_name_list)
            )
        return await self.arequest("GET", "/getAutoScalingGroupList", params=params)

    def get_auto_scaling_group_detail(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            responseFormatType="json",
        )
        return self.request("GET", "/getAutoScalingGroupDetail", params=params)

    async def aget_auto_scaling_group_detail(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            responseFormatType="json",
        )
        return await self.arequest("GET", "/getAutoScalingGroupDetail", params=params)

    def set_desired_capacity(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        desired_capacity: int,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            desiredCapacity=desired_capacity,
            responseFormatType="json",
        )
        return self.request("POST", "/setDesiredCapacity", data=data)

    async def aset_desired_capacity(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        desired_capacity: int,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            desiredCapacity=desired_capacity,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/setDesiredCapacity", data=data)

    def resume_processes(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        scaling_process_code_list: list[str],
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            responseFormatType="json",
        )
        data.update(_list_params("scalingProcessCodeList", scaling_process_code_list))
        return self.request("POST", "/resumeProcesses", data=data)

    async def aresume_processes(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        scaling_process_code_list: list[str],
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            responseFormatType="json",
        )
        data.update(_list_params("scalingProcessCodeList", scaling_process_code_list))
        return await self.arequest("POST", "/resumeProcesses", data=data)

    def suspend_processes(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        scaling_process_code_list: list[str],
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            responseFormatType="json",
        )
        data.update(_list_params("scalingProcessCodeList", scaling_process_code_list))
        return self.request("POST", "/suspendProcesses", data=data)

    async def asuspend_processes(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        scaling_process_code_list: list[str],
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            responseFormatType="json",
        )
        data.update(_list_params("scalingProcessCodeList", scaling_process_code_list))
        return await self.arequest("POST", "/suspendProcesses", data=data)

    def get_scaling_process_type_list(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(regionCode=region_code, responseFormatType="json")
        return self.request("GET", "/getScalingProcessTypeList", params=params)

    async def aget_scaling_process_type_list(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(regionCode=region_code, responseFormatType="json")
        return await self.arequest("GET", "/getScalingProcessTypeList", params=params)

    # --- Scaling Policy ---

    def put_scaling_policy(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        adjustment_type_code: str,
        scaling_adjustment: int,
        policy_no: str | None = None,
        policy_name: str | None = None,
        min_adjustment_step: int | None = None,
        cool_down: int | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            adjustmentTypeCode=adjustment_type_code,
            scalingAdjustment=scaling_adjustment,
            policyNo=policy_no,
            policyName=policy_name,
            minAdjustmentStep=min_adjustment_step,
            coolDown=cool_down,
            responseFormatType="json",
        )
        return self.request("POST", "/putScalingPolicy", data=data)

    async def aput_scaling_policy(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        adjustment_type_code: str,
        scaling_adjustment: int,
        policy_no: str | None = None,
        policy_name: str | None = None,
        min_adjustment_step: int | None = None,
        cool_down: int | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            adjustmentTypeCode=adjustment_type_code,
            scalingAdjustment=scaling_adjustment,
            policyNo=policy_no,
            policyName=policy_name,
            minAdjustmentStep=min_adjustment_step,
            coolDown=cool_down,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/putScalingPolicy", data=data)

    def delete_scaling_policy(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        policy_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            policyNo=policy_no,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteScalingPolicy", data=data)

    async def adelete_scaling_policy(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        policy_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            policyNo=policy_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deleteScalingPolicy", data=data)

    def execute_policy(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        policy_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            policyNo=policy_no,
            responseFormatType="json",
        )
        return self.request("POST", "/executePolicy", data=data)

    async def aexecute_policy(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        policy_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            policyNo=policy_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/executePolicy", data=data)

    def get_auto_scaling_policy_list(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        policy_no_list: list[str] | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            responseFormatType="json",
        )
        if policy_no_list:
            params.update(_list_params("policyNoList", policy_no_list))
        return self.request("GET", "/getAutoScalingPolicyList", params=params)

    async def aget_auto_scaling_policy_list(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        policy_no_list: list[str] | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            responseFormatType="json",
        )
        if policy_no_list:
            params.update(_list_params("policyNoList", policy_no_list))
        return await self.arequest("GET", "/getAutoScalingPolicyList", params=params)

    def get_adjustment_type_list(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(regionCode=region_code, responseFormatType="json")
        return self.request("GET", "/getAdjustmentTypeList", params=params)

    async def aget_adjustment_type_list(
        self,
        *,
        region_code: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(regionCode=region_code, responseFormatType="json")
        return await self.arequest("GET", "/getAdjustmentTypeList", params=params)

    # --- Scheduled Action ---

    def put_scheduled_update_group_action(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        min_size: int,
        max_size: int,
        scheduled_action_no: str | None = None,
        scheduled_action_name: str | None = None,
        desired_capacity: int | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        recurrence: str | None = None,
        time_zone: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            minSize=min_size,
            maxSize=max_size,
            scheduledActionNo=scheduled_action_no,
            scheduledActionName=scheduled_action_name,
            desiredCapacity=desired_capacity,
            startTime=start_time,
            endTime=end_time,
            recurrence=recurrence,
            timeZone=time_zone,
            responseFormatType="json",
        )
        return self.request("POST", "/putScheduledUpdateGroupAction", data=data)

    async def aput_scheduled_update_group_action(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        min_size: int,
        max_size: int,
        scheduled_action_no: str | None = None,
        scheduled_action_name: str | None = None,
        desired_capacity: int | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        recurrence: str | None = None,
        time_zone: str | None = None,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            minSize=min_size,
            maxSize=max_size,
            scheduledActionNo=scheduled_action_no,
            scheduledActionName=scheduled_action_name,
            desiredCapacity=desired_capacity,
            startTime=start_time,
            endTime=end_time,
            recurrence=recurrence,
            timeZone=time_zone,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/putScheduledUpdateGroupAction", data=data)

    def delete_scheduled_action(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        scheduled_action_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            scheduledActionNo=scheduled_action_no,
            responseFormatType="json",
        )
        return self.request("POST", "/deleteScheduledAction", data=data)

    async def adelete_scheduled_action(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        scheduled_action_no: str,
    ) -> dict[str, Any]:
        data = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            scheduledActionNo=scheduled_action_no,
            responseFormatType="json",
        )
        return await self.arequest("POST", "/deleteScheduledAction", data=data)

    def get_scheduled_action_list(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        scheduled_action_no_list: list[str] | None = None,
        scheduled_action_name_list: list[str] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            startTime=start_time,
            endTime=end_time,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        if scheduled_action_no_list:
            params.update(
                _list_params("scheduledActionNoList", scheduled_action_no_list)
            )
        if scheduled_action_name_list:
            params.update(
                _list_params("scheduledActionNameList", scheduled_action_name_list)
            )
        return self.request("GET", "/getScheduledActionList", params=params)

    async def aget_scheduled_action_list(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        scheduled_action_no_list: list[str] | None = None,
        scheduled_action_name_list: list[str] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
        sorted_by: str | None = None,
        sorting_order: str | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            startTime=start_time,
            endTime=end_time,
            pageNo=page_no,
            pageSize=page_size,
            sortedBy=sorted_by,
            sortingOrder=sorting_order,
            responseFormatType="json",
        )
        if scheduled_action_no_list:
            params.update(
                _list_params("scheduledActionNoList", scheduled_action_no_list)
            )
        if scheduled_action_name_list:
            params.update(
                _list_params("scheduledActionNameList", scheduled_action_name_list)
            )
        return await self.arequest("GET", "/getScheduledActionList", params=params)

    # --- Activity / Logs ---

    def get_auto_scaling_activity_log_list(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        activity_no_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if activity_no_list:
            params.update(_list_params("activityNoList", activity_no_list))
        return self.request("GET", "/getAutoScalingActivityLogList", params=params)

    async def aget_auto_scaling_activity_log_list(
        self,
        *,
        region_code: str | None = None,
        auto_scaling_group_no: str,
        activity_no_list: list[str] | None = None,
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        params = _build_params(
            regionCode=region_code,
            autoScalingGroupNo=auto_scaling_group_no,
            pageNo=page_no,
            pageSize=page_size,
            responseFormatType="json",
        )
        if activity_no_list:
            params.update(_list_params("activityNoList", activity_no_list))
        return await self.arequest(
            "GET", "/getAutoScalingActivityLogList", params=params
        )
