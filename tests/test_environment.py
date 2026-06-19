from __future__ import annotations

import pytest

from ncp_api.environment import BASE_URLS, NcpEnv


def test_ncp_env_values() -> None:
    assert NcpEnv.PUBLIC == "public"
    assert NcpEnv.GOV == "gov"
    assert NcpEnv.FIN == "fin"


def test_ncp_env_from_string() -> None:
    assert NcpEnv("public") is NcpEnv.PUBLIC
    assert NcpEnv("gov") is NcpEnv.GOV
    assert NcpEnv("fin") is NcpEnv.FIN


def test_ncp_env_invalid_raises() -> None:
    with pytest.raises(ValueError):
        NcpEnv("invalid")


def test_base_urls_keys() -> None:
    assert set(BASE_URLS.keys()) == {NcpEnv.PUBLIC, NcpEnv.GOV, NcpEnv.FIN}


def test_base_urls_public() -> None:
    assert BASE_URLS[NcpEnv.PUBLIC] == "https://ncloud.apigw.ntruss.com"


def test_base_urls_gov() -> None:
    assert BASE_URLS[NcpEnv.GOV] == "https://ncloud.apigw.gov-ntruss.com"


def test_base_urls_fin() -> None:
    assert BASE_URLS[NcpEnv.FIN] == "https://ncloud.apigw.fin-ntruss.com"
