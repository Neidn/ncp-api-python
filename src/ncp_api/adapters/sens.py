from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

SENS_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://sens.apigw.ntruss.com",
    NcpEnv.GOV: "https://sens.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://sens.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class SensApi(NcpHttpAdapter):
    """SENS (Simple & Easy Notification Service) SMS. Sig-v2, REST + JSON."""

    path_prefix: ClassVar[str] = "/sms/v2/services"

    def send_sms(
        self,
        *,
        service_id: str,
        type: str,
        from_: str,
        content: str,
        messages: list[dict[str, Any]],
        content_type: str | None = None,
        country_code: str | None = None,
        subject: str | None = None,
        files: list[dict[str, Any]] | None = None,
        reserve_time: str | None = None,
        reserve_time_zone: str | None = None,
    ) -> dict[str, Any]:
        body = _body(
            type=type,
            contentType=content_type,
            countryCode=country_code,
            **{"from": from_},
            subject=subject,
            content=content,
            messages=messages,
            files=files,
            reserveTime=reserve_time,
            reserveTimeZone=reserve_time_zone,
        )
        return self.request("POST", f"/{service_id}/messages", json=body)

    async def asend_sms(
        self,
        *,
        service_id: str,
        type: str,
        from_: str,
        content: str,
        messages: list[dict[str, Any]],
        content_type: str | None = None,
        country_code: str | None = None,
        subject: str | None = None,
        files: list[dict[str, Any]] | None = None,
        reserve_time: str | None = None,
        reserve_time_zone: str | None = None,
    ) -> dict[str, Any]:
        body = _body(
            type=type,
            contentType=content_type,
            countryCode=country_code,
            **{"from": from_},
            subject=subject,
            content=content,
            messages=messages,
            files=files,
            reserveTime=reserve_time,
            reserveTimeZone=reserve_time_zone,
        )
        return await self.arequest("POST", f"/{service_id}/messages", json=body)
