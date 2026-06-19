from __future__ import annotations

import pytest

from ncp_api.exceptions import NcpApiError, NcpAuthError, NcpError, NcpNetworkError


def test_ncp_error_is_exception() -> None:
    assert issubclass(NcpError, Exception)


def test_ncp_auth_error_is_ncp_error() -> None:
    assert issubclass(NcpAuthError, NcpError)


def test_ncp_network_error_is_ncp_error() -> None:
    assert issubclass(NcpNetworkError, NcpError)


def test_ncp_api_error_is_ncp_error() -> None:
    assert issubclass(NcpApiError, NcpError)


def test_ncp_api_error_has_attrs() -> None:
    err = NcpApiError(status_code=400, error_code="1001", message="bad request")
    assert err.status_code == 400
    assert err.error_code == "1001"
    assert err.message == "bad request"
    assert str(err) == "bad request"


def test_ncp_api_error_inherits_message() -> None:
    err = NcpApiError(status_code=500, error_code="9999", message="server error")
    with pytest.raises(NcpError):
        raise err
