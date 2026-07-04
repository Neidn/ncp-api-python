from __future__ import annotations

import base64
import hashlib
import hmac


class HmacSigner:
    def __init__(self, access_key: str, secret_key: str) -> None:
        self._access_key = access_key
        self._secret_key = secret_key

    def sign(self, method: str, url: str, timestamp: int) -> dict[str, str]:
        """Return NCP HMAC-SHA256 auth headers for one request.

        Args:
            method: HTTP method in uppercase, e.g. "GET".
            url: Path + query string only, e.g. "/vserver/v2/list?region=KR".
            timestamp: Unix time in milliseconds.
        """
        string_to_sign = f"{method} {url}\n{timestamp}\n{self._access_key}"
        mac = hmac.new(
            self._secret_key.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha256,
        )
        signature = base64.b64encode(mac.digest()).decode("utf-8")
        return {
            "x-ncp-apigw-timestamp": str(timestamp),
            "x-ncp-iam-access-key": self._access_key,
            "x-ncp-apigw-signature-v2": signature,
        }
