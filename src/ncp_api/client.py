from __future__ import annotations

import os

from ncp_api.adapters.fin import FinAdapter
from ncp_api.adapters.gov import GovAdapter
from ncp_api.adapters.public import PublicAdapter
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
