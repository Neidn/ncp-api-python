from __future__ import annotations

from ncp_api.adapters.auto_scaling import AutoScalingApi
from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.adapters.block_storage import BlockStorageApi
from ncp_api.adapters.cache import CloudCacheApi, CloudRedisApi
from ncp_api.adapters.cdn import CdnApi
from ncp_api.adapters.cdss import CDSS_BASE_URLS, CdssApi
from ncp_api.adapters.classic_auto_scaling import ClassicAutoScalingApi
from ncp_api.adapters.cloud_db import CloudDbApi
from ncp_api.adapters.cloud_insight import CLOUD_INSIGHT_BASE_URLS, CloudInsightApi
from ncp_api.adapters.global_dns import GLOBAL_DNS_BASE_URLS, GlobalDnsApi
from ncp_api.adapters.hadoop import HadoopApi
from ncp_api.adapters.load_balancer import LoadBalancerApi
from ncp_api.adapters.mongodb import CloudMongoDbApi
from ncp_api.adapters.mssql import MssqlApi
from ncp_api.adapters.mysql import CloudMysqlApi
from ncp_api.adapters.nas import NasApi
from ncp_api.adapters.nks import NKS_BASE_URLS, NksApi
from ncp_api.adapters.object_storage import OBJECT_STORAGE_BASE_URLS, ObjectStorageApi
from ncp_api.adapters.postgresql import CloudPostgresqlApi
from ncp_api.adapters.search_engine import SEARCH_ENGINE_BASE_URLS, SearchEngineApi
from ncp_api.adapters.server import ServerApi
from ncp_api.adapters.source_build import SOURCE_BUILD_BASE_URLS, SourceBuildApi
from ncp_api.adapters.source_commit import SOURCE_COMMIT_BASE_URLS, SourceCommitApi
from ncp_api.adapters.source_deploy import (
    VPC_SOURCE_DEPLOY_BASE_URLS,
    VpcSourceDeployApi,
)
from ncp_api.adapters.source_pipeline import (
    SOURCE_PIPELINE_BASE_URLS,
    VPC_SOURCE_PIPELINE_BASE_URLS,
    SourcePipelineApi,
)
from ncp_api.adapters.vpc import VpcApi
from ncp_api.auth import HmacSigner
from ncp_api.environment import NcpEnv


class PublicAdapter(NcpHttpAdapter):
    """Adapter for NCP Public cloud environment."""

    def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
        super().__init__(env_base_url, signer)
        self.server = ServerApi(env_base_url, signer)
        self.block_storage = BlockStorageApi(env_base_url, signer)
        self.global_dns = GlobalDnsApi(GLOBAL_DNS_BASE_URLS[NcpEnv.PUBLIC], signer)
        self.load_balancer = LoadBalancerApi(env_base_url, signer)
        self.nas = NasApi(env_base_url, signer)
        self.object_storage = ObjectStorageApi(
            OBJECT_STORAGE_BASE_URLS[NcpEnv.PUBLIC], signer
        )
        self.vpc = VpcApi(env_base_url, signer)
        self.cache = CloudCacheApi(env_base_url, signer)
        self.redis = CloudRedisApi(env_base_url, signer)
        self.cloud_insight = CloudInsightApi(
            CLOUD_INSIGHT_BASE_URLS[NcpEnv.PUBLIC], signer
        )
        self.mysql = CloudMysqlApi(env_base_url, signer)
        self.mongodb = CloudMongoDbApi(env_base_url, signer)
        self.postgresql = CloudPostgresqlApi(env_base_url, signer)
        self.nks = NksApi(NKS_BASE_URLS[NcpEnv.PUBLIC], signer)
        # New adapters
        self.auto_scaling = AutoScalingApi(env_base_url, signer)
        self.hadoop = HadoopApi(env_base_url, signer)
        self.mssql = MssqlApi(env_base_url, signer)
        self.cdn = CdnApi(env_base_url, signer)
        self.cdss = CdssApi(CDSS_BASE_URLS[NcpEnv.PUBLIC], signer)
        self.search_engine = SearchEngineApi(
            SEARCH_ENGINE_BASE_URLS[NcpEnv.PUBLIC], signer
        )
        self.classic_auto_scaling = ClassicAutoScalingApi(env_base_url, signer)
        self.cloud_db = CloudDbApi(env_base_url, signer)
        self.source_commit = SourceCommitApi(
            SOURCE_COMMIT_BASE_URLS[NcpEnv.PUBLIC], signer
        )
        self.source_build = SourceBuildApi(
            SOURCE_BUILD_BASE_URLS[NcpEnv.PUBLIC], signer
        )
        self.source_pipeline = SourcePipelineApi(
            SOURCE_PIPELINE_BASE_URLS[NcpEnv.PUBLIC], signer
        )
        self.vpc_source_pipeline = SourcePipelineApi(
            VPC_SOURCE_PIPELINE_BASE_URLS[NcpEnv.PUBLIC], signer
        )
        self.vpc_source_deploy = VpcSourceDeployApi(
            VPC_SOURCE_DEPLOY_BASE_URLS[NcpEnv.PUBLIC], signer
        )
