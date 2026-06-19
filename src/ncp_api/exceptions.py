from __future__ import annotations


class NcpError(Exception):
    """Base exception for all NCP API errors."""


class NcpAuthError(NcpError):
    """Raised on 401 responses or HMAC signature failures."""


class NcpApiError(NcpError):
    """Raised on non-2xx API responses."""

    def __init__(self, *, status_code: int, error_code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message


class NcpNetworkError(NcpError):
    """Raised on connection failures or timeouts."""
