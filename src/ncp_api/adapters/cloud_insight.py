from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, cast

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.environment import NcpEnv

CLOUD_INSIGHT_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://cw.apigw.ntruss.com",
    NcpEnv.GOV: "https://cw.apigw.gov-ntruss.com",  # TBD: confirm from gov docs
    NcpEnv.FIN: "https://cw.apigw.fin-ntruss.com",  # TBD: confirm from fin docs
}


@dataclass
class MetricInfo:
    prod_key: str
    metric: str
    interval: str  # Min1, Min5, Min30, Hour2, Day1
    dimensions: dict[str, str]
    aggregation: str = "AVG"  # COUNT, SUM, MAX, MIN, AVG
    query_aggregation: str | None = None


def _build_request_body(
    time_start: int,
    time_end: int,
    metric_info_list: list[MetricInfo],
) -> dict[str, Any]:
    metrics: list[dict[str, Any]] = []
    for info in metric_info_list:
        m: dict[str, Any] = {
            "prodKey": info.prod_key,
            "metric": info.metric,
            "interval": info.interval,
            "dimensions": info.dimensions,
            "aggregation": info.aggregation,
        }
        if info.query_aggregation is not None:
            m["queryAggregation"] = info.query_aggregation
        metrics.append(m)
    return {
        "timeStart": time_start,
        "timeEnd": time_end,
        "metricInfoList": metrics,
    }


class CloudInsightApi(NcpHttpAdapter):
    path_prefix: ClassVar[str] = "/cw_fea/real/cw/api"

    def query_data_multiple(
        self,
        *,
        time_start: int,
        time_end: int,
        metric_info_list: list[MetricInfo],
    ) -> list[dict[str, Any]]:
        body = _build_request_body(time_start, time_end, metric_info_list)
        raw = self.request("POST", "/data/query/multiple", json=body)
        return cast(list[dict[str, Any]], raw)

    async def aquery_data_multiple(
        self,
        *,
        time_start: int,
        time_end: int,
        metric_info_list: list[MetricInfo],
    ) -> list[dict[str, Any]]:
        body = _build_request_body(time_start, time_end, metric_info_list)
        raw = await self.arequest("POST", "/data/query/multiple", json=body)
        return cast(list[dict[str, Any]], raw)
