from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

CLOUD_OUTBOUND_MAILER_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://mail.apigw.ntruss.com",
    NcpEnv.GOV: "https://mail.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://mail.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def _build_params(**kwargs: Any) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None}


class CloudOutboundMailerApi(NcpHttpAdapter):
    """Cloud Outbound Mailer. Sig-v2, REST + JSON."""

    path_prefix: ClassVar[str] = "/api/v1"

    def create_mail(
        self,
        *,
        recipients: list[dict[str, Any]],
        sender_address: str | None = None,
        sender_name: str | None = None,
        template_sid: int | None = None,
        title: str | None = None,
        body: str | None = None,
        individual: bool | None = None,
        confirm_and_send: bool | None = None,
        advertising: bool | None = None,
        parameters: dict[str, Any] | None = None,
        use_basic_unsubscribe_msg: bool | None = None,
        unsubscribe_message: str | None = None,
        reservation: str | None = None,
        reservation_utc: str | None = None,
        attach_file_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        payload = _body(
            senderAddress=sender_address,
            senderName=sender_name,
            templateSid=template_sid,
            title=title,
            body=body,
            recipients=recipients,
            individual=individual,
            confirmAndSend=confirm_and_send,
            advertising=advertising,
            parameters=parameters,
            useBasicUnsubscribeMsg=use_basic_unsubscribe_msg,
            unsubscribeMessage=unsubscribe_message,
            reservation=reservation,
            reservationUtc=reservation_utc,
            attachFileIds=attach_file_ids,
        )
        return self.request("POST", "/mails", json=payload)

    async def acreate_mail(
        self,
        *,
        recipients: list[dict[str, Any]],
        sender_address: str | None = None,
        sender_name: str | None = None,
        template_sid: int | None = None,
        title: str | None = None,
        body: str | None = None,
        individual: bool | None = None,
        confirm_and_send: bool | None = None,
        advertising: bool | None = None,
        parameters: dict[str, Any] | None = None,
        use_basic_unsubscribe_msg: bool | None = None,
        unsubscribe_message: str | None = None,
        reservation: str | None = None,
        reservation_utc: str | None = None,
        attach_file_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        payload = _body(
            senderAddress=sender_address,
            senderName=sender_name,
            templateSid=template_sid,
            title=title,
            body=body,
            recipients=recipients,
            individual=individual,
            confirmAndSend=confirm_and_send,
            advertising=advertising,
            parameters=parameters,
            useBasicUnsubscribeMsg=use_basic_unsubscribe_msg,
            unsubscribeMessage=unsubscribe_message,
            reservation=reservation,
            reservationUtc=reservation_utc,
            attachFileIds=attach_file_ids,
        )
        return await self.arequest("POST", "/mails", json=payload)

    def _get_mail_request_list_params(
        self,
        *,
        start_utc: int | None,
        start_date_time: str | None,
        end_utc: int | None,
        end_date_time: str | None,
        request_id: str | None,
        mail_id: str | None,
        dispatch_type: str | None,
        title: str | None,
        template_sid: int | None,
        send_status: str | None,
        page: int | None,
        size: int | None,
    ) -> dict[str, str]:
        return _build_params(
            startUtc=start_utc,
            startDateTime=start_date_time,
            endUtc=end_utc,
            endDateTime=end_date_time,
            requestId=request_id,
            mailId=mail_id,
            dispatchType=dispatch_type,
            title=title,
            templateSid=template_sid,
            sendStatus=send_status,
            page=page,
            size=size,
        )

    def get_mail_request_list(
        self,
        *,
        start_utc: int | None = None,
        start_date_time: str | None = None,
        end_utc: int | None = None,
        end_date_time: str | None = None,
        request_id: str | None = None,
        mail_id: str | None = None,
        dispatch_type: str | None = None,
        title: str | None = None,
        template_sid: int | None = None,
        send_status: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_mail_request_list_params(
            start_utc=start_utc,
            start_date_time=start_date_time,
            end_utc=end_utc,
            end_date_time=end_date_time,
            request_id=request_id,
            mail_id=mail_id,
            dispatch_type=dispatch_type,
            title=title,
            template_sid=template_sid,
            send_status=send_status,
            page=page,
            size=size,
        )
        return self.request("GET", "/mails/requests", params=params)

    async def aget_mail_request_list(
        self,
        *,
        start_utc: int | None = None,
        start_date_time: str | None = None,
        end_utc: int | None = None,
        end_date_time: str | None = None,
        request_id: str | None = None,
        mail_id: str | None = None,
        dispatch_type: str | None = None,
        title: str | None = None,
        template_sid: int | None = None,
        send_status: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> dict[str, Any]:
        params = self._get_mail_request_list_params(
            start_utc=start_utc,
            start_date_time=start_date_time,
            end_utc=end_utc,
            end_date_time=end_date_time,
            request_id=request_id,
            mail_id=mail_id,
            dispatch_type=dispatch_type,
            title=title,
            template_sid=template_sid,
            send_status=send_status,
            page=page,
            size=size,
        )
        return await self.arequest("GET", "/mails/requests", params=params)
