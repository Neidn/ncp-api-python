from __future__ import annotations

import os
from types import TracebackType

from ncp_api.adapters.fin import FinAdapter
from ncp_api.adapters.gov import GovAdapter
from ncp_api.adapters.public import PublicAdapter
from ncp_api.adapters.block_storage import BlockStorageApi
from ncp_api.adapters.cache import CloudCacheApi, CloudRedisApi
from ncp_api.adapters.cloud_insight import CloudInsightApi
from ncp_api.adapters.mongodb import CloudMongoDbApi
from ncp_api.adapters.mysql import CloudMysqlApi
from ncp_api.adapters.load_balancer import LoadBalancerApi
from ncp_api.adapters.nas import NasApi
from ncp_api.adapters.nks import NksApi
from ncp_api.adapters.object_storage import ObjectStorageApi
from ncp_api.adapters.postgresql import CloudPostgresqlApi
from ncp_api.adapters.server import ServerApi
from ncp_api.adapters.vpc import VpcApi
from ncp_api.auth import HmacSigner
from ncp_api.environment import BASE_URLS, NcpEnv


class NcpClient:
    """Entry point for the NCP API client.

    Environment resolution order:
    1. ``env`` constructor parameter
    2. ``NCP_ENV`` environment variable
    3. Default: ``"public"``
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        env: str | NcpEnv | None = None,
    ) -> None:
        resolved = NcpEnv(env or os.environ.get("NCP_ENV", "public"))
        signer = HmacSigner(access_key, secret_key)
        base_url = BASE_URLS[resolved]

        if resolved is NcpEnv.PUBLIC:
            self._adapter: PublicAdapter | GovAdapter | FinAdapter = PublicAdapter(
                base_url, signer
            )
        elif resolved is NcpEnv.GOV:
            self._adapter = GovAdapter(base_url, signer)
        else:
            self._adapter = FinAdapter(base_url, signer)

    @property
    def server(self) -> ServerApi:
        return self._adapter.server

    @property
    def block_storage(self) -> BlockStorageApi:
        return self._adapter.block_storage

    @property
    def load_balancer(self) -> LoadBalancerApi:
        return self._adapter.load_balancer

    @property
    def nas(self) -> NasApi:
        return self._adapter.nas

    @property
    def object_storage(self) -> ObjectStorageApi:
        return self._adapter.object_storage

    @property
    def vpc(self) -> VpcApi:
        return self._adapter.vpc

    @property
    def cache(self) -> CloudCacheApi:
        return self._adapter.cache

    @property
    def redis(self) -> CloudRedisApi:
        return self._adapter.redis

    @property
    def cloud_insight(self) -> CloudInsightApi:
        return self._adapter.cloud_insight

    @property
    def mysql(self) -> CloudMysqlApi:
        return self._adapter.mysql

    @property
    def mongodb(self) -> CloudMongoDbApi:
        return self._adapter.mongodb

    @property
    def postgresql(self) -> CloudPostgresqlApi:
        return self._adapter.postgresql

    @property
    def nks(self) -> NksApi:
        return self._adapter.nks

    def close(self) -> None:
        self._adapter.close()

    async def aclose(self) -> None:
        await self._adapter.aclose()

    def __enter__(self) -> NcpClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    async def __aenter__(self) -> NcpClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()
