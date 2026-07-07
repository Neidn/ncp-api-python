from __future__ import annotations

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.adapters.cloud_insight import CLOUD_INSIGHT_BASE_URLS, CloudInsightApi
from ncp_api.adapters.mongodb import CloudMongoDbApi
from ncp_api.adapters.mysql import CloudMysqlApi
from ncp_api.adapters.server import ServerApi
from ncp_api.auth import HmacSigner
from ncp_api.environment import NcpEnv


class GovAdapter(NcpHttpAdapter):
    """Adapter for NCP Government cloud environment."""

    def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
        super().__init__(env_base_url, signer)
        self.server = ServerApi(env_base_url, signer)
        self.cloud_insight = CloudInsightApi(CLOUD_INSIGHT_BASE_URLS[NcpEnv.GOV], signer)
        self.mysql = CloudMysqlApi(env_base_url, signer)
        self.mongodb = CloudMongoDbApi(env_base_url, signer)
