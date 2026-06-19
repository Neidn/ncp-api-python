from __future__ import annotations

import pytest

from ncp_api import (
    NcpApiError,
    NcpAuthError,
    NcpClient,
    NcpEnv,
    NcpError,
    NcpNetworkError,
)
from ncp_api.adapters.fin import FinAdapter
from ncp_api.adapters.gov import GovAdapter
from ncp_api.adapters.public import PublicAdapter
from ncp_api.environment import BASE_URLS


def test_default_env_is_public() -> None:
    client = NcpClient(access_key="k", secret_key="s")
    assert isinstance(client._adapter, PublicAdapter)


def test_env_param_string_public() -> None:
    client = NcpClient(access_key="k", secret_key="s", env="public")
    assert isinstance(client._adapter, PublicAdapter)


def test_env_param_string_gov() -> None:
    client = NcpClient(access_key="k", secret_key="s", env="gov")
    assert isinstance(client._adapter, GovAdapter)


def test_env_param_string_fin() -> None:
    client = NcpClient(access_key="k", secret_key="s", env="fin")
    assert isinstance(client._adapter, FinAdapter)


def test_env_param_enum_public() -> None:
    client = NcpClient(access_key="k", secret_key="s", env=NcpEnv.PUBLIC)
    assert isinstance(client._adapter, PublicAdapter)


def test_env_param_enum_gov() -> None:
    client = NcpClient(access_key="k", secret_key="s", env=NcpEnv.GOV)
    assert isinstance(client._adapter, GovAdapter)


def test_env_param_enum_fin() -> None:
    client = NcpClient(access_key="k", secret_key="s", env=NcpEnv.FIN)
    assert isinstance(client._adapter, FinAdapter)


def test_env_from_env_var_gov(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NCP_ENV", "gov")
    client = NcpClient(access_key="k", secret_key="s")
    assert isinstance(client._adapter, GovAdapter)


def test_env_from_env_var_fin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NCP_ENV", "fin")
    client = NcpClient(access_key="k", secret_key="s")
    assert isinstance(client._adapter, FinAdapter)


def test_env_param_overrides_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NCP_ENV", "gov")
    client = NcpClient(access_key="k", secret_key="s", env="fin")
    assert isinstance(client._adapter, FinAdapter)


def test_invalid_env_raises_value_error() -> None:
    with pytest.raises(ValueError):
        NcpClient(access_key="k", secret_key="s", env="invalid")


def test_adapter_base_url_matches_env_public() -> None:
    client = NcpClient(access_key="k", secret_key="s", env="public")
    assert client._adapter.base_url == BASE_URLS[NcpEnv.PUBLIC]


def test_adapter_base_url_matches_env_gov() -> None:
    client = NcpClient(access_key="k", secret_key="s", env="gov")
    assert client._adapter.base_url == BASE_URLS[NcpEnv.GOV]


def test_imports_from_package_root() -> None:
    assert NcpClient is not None
    assert NcpEnv is not None
    assert NcpError is not None
    assert NcpAuthError is not None
    assert NcpApiError is not None
    assert NcpNetworkError is not None
