from __future__ import annotations

import pytest

from ncp_api.exceptions import (
    NcpApiError,
    NcpAuthError,
    NcpError,
    NcpNetworkError,
    NcpRateLimitError,
)


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


def test_ncp_auth_error_has_error_code() -> None:
    err = NcpAuthError("Permission denied", error_code="210")
    assert err.error_code == "210"
    assert str(err) == "Permission denied"


def test_ncp_auth_error_default_error_code() -> None:
    err = NcpAuthError("Authentication failed")
    assert err.error_code == ""


def test_ncp_rate_limit_error_is_api_error() -> None:
    assert issubclass(NcpRateLimitError, NcpApiError)


def test_ncp_rate_limit_error_has_attrs() -> None:
    err = NcpRateLimitError(status_code=429, error_code="400", message="Quota Exceeded")
    assert err.status_code == 429
    assert err.error_code == "400"
    assert err.message == "Quota Exceeded"
