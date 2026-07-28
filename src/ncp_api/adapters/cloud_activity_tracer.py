from __future__ import annotations

from typing import Any, ClassVar

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

CLOUD_ACTIVITY_TRACER_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://cloudactivitytracer.apigw.ntruss.com",
    NcpEnv.GOV: "https://cloudactivitytracer.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://cloudactivitytracer.apigw.fin-ntruss.com",
}


def _body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class CloudActivityTracerApi(NcpHttpAdapter):
    """Cloud Activity Tracer. Sig-v2, REST + JSON."""

    path_prefix: ClassVar[str] = "/api/v1"

    def get_activity_list(
        self,
        *,
        from_event_time: int | None = None,
        to_event_time: int | None = None,
        nrn: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> dict[str, Any]:
        body = _body(
            fromEventTime=from_event_time,
            toEventTime=to_event_time,
            nrn=nrn,
            page=page,
            size=size,
        )
        return self.request("POST", "/activities", json=body)

    async def aget_activity_list(
        self,
        *,
        from_event_time: int | None = None,
        to_event_time: int | None = None,
        nrn: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> dict[str, Any]:
        body = _body(
            fromEventTime=from_event_time,
            toEventTime=to_event_time,
            nrn=nrn,
            page=page,
            size=size,
        )
        return await self.arequest("POST", "/activities", json=body)
