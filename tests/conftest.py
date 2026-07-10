from __future__ import annotations

import os
from pathlib import Path

import pytest

# Load .env from project root if it exists (no-op if missing)
_env_file = Path(__file__).parent.parent / ".env"
if _env_file.exists():
    from dotenv import load_dotenv

    load_dotenv(_env_file)


@pytest.fixture
def live_client():
    """Return a real NcpClient when .env provides credentials; skip otherwise."""
    access_key = os.environ.get("NCP_ACCESS_KEY")
    secret_key = os.environ.get("NCP_SECRET_KEY")
    env = os.environ.get("NCP_ENV", "public")

    if not access_key or not secret_key:
        pytest.skip("NCP_ACCESS_KEY / NCP_SECRET_KEY not set — skipping live test")

    from ncp_api.client import NcpClient

    client = NcpClient(access_key=access_key, secret_key=secret_key, env=env)
    yield client
    client.close()
