from __future__ import annotations

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.adapters.block_storage import BlockStorageApi
from ncp_api.adapters.cache import CloudCacheApi, CloudRedisApi
from ncp_api.adapters.cloud_insight import CLOUD_INSIGHT_BASE_URLS, CloudInsightApi
from ncp_api.adapters.mongodb import CloudMongoDbApi
from ncp_api.adapters.mysql import CloudMysqlApi
from ncp_api.adapters.load_balancer import LoadBalancerApi
from ncp_api.adapters.nas import NasApi
from ncp_api.adapters.nks import NKS_BASE_URLS, NksApi
from ncp_api.adapters.object_storage import OBJECT_STORAGE_BASE_URLS, ObjectStorageApi
from ncp_api.adapters.postgresql import CloudPostgresqlApi
from ncp_api.adapters.server import ServerApi
from ncp_api.adapters.vpc import VpcApi
from ncp_api.auth import HmacSigner
from ncp_api.environment import NcpEnv


class FinAdapter(NcpHttpAdapter):
    """Adapter for NCP Financial cloud environment."""

    def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
        super().__init__(env_base_url, signer)
        self.server = ServerApi(env_base_url, signer)
        self.block_storage = BlockStorageApi(env_base_url, signer)
        self.load_balancer = LoadBalancerApi(env_base_url, signer)
        self.nas = NasApi(env_base_url, signer)
        self.object_storage = ObjectStorageApi(OBJECT_STORAGE_BASE_URLS[NcpEnv.FIN], signer)
        self.vpc = VpcApi(env_base_url, signer)
        self.cache = CloudCacheApi(env_base_url, signer)
        self.redis = CloudRedisApi(env_base_url, signer)
        self.cloud_insight = CloudInsightApi(CLOUD_INSIGHT_BASE_URLS[NcpEnv.FIN], signer)
        self.mysql = CloudMysqlApi(env_base_url, signer)
        self.mongodb = CloudMongoDbApi(env_base_url, signer)
        self.postgresql = CloudPostgresqlApi(env_base_url, signer)
        self.nks = NksApi(NKS_BASE_URLS[NcpEnv.FIN], signer)
