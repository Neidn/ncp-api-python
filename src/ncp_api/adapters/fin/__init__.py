from __future__ import annotations

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.adapters.server import ServerApi
from ncp_api.auth import HmacSigner


class FinAdapter(NcpHttpAdapter):
    """Adapter for NCP Financial cloud environment."""

    def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
        super().__init__(env_base_url, signer)
        self.server = ServerApi(env_base_url, signer)
