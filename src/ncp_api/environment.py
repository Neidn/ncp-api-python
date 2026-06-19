from __future__ import annotations

from enum import Enum


class NcpEnv(str, Enum):
    PUBLIC = "public"
    GOV = "gov"
    FIN = "fin"


BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://ncloud.apigw.ntruss.com",
    NcpEnv.GOV: "https://ncloud.apigw.gov-ntruss.com",
    NcpEnv.FIN: "https://ncloud.apigw.fin-ntruss.com",
}
