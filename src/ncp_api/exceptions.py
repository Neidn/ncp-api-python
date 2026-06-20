from __future__ import annotations


class NcpError(Exception):
    """Base exception for all NCP API errors."""


class NcpAuthError(NcpError):
    """Raised on HTTP 401.

    error_code 200 = invalid credentials, 210 = insufficient permissions.
    """

    def __init__(self, message: str, *, error_code: str = "") -> None:
        super().__init__(message)
        self.error_code = error_code


class NcpApiError(NcpError):
    """Raised on non-2xx API responses."""

    def __init__(self, *, status_code: int, error_code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message


class NcpRateLimitError(NcpApiError):
    """Raised on HTTP 429.

    error_code 400 = quota exceeded, 410 = throttle limited, 420 = rate limited.
    """


class NcpNetworkError(NcpError):
    """Raised on connection failures or timeouts."""
