from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timezone


class AwsSigV4Signer:
    """AWS Signature Version 4 signer for NCP Object Storage."""

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        region: str = "kr-standard",
        service: str = "s3",
    ) -> None:
        self._access_key = access_key
        self._secret_key = secret_key
        self._region = region
        self._service = service

    def _hmac(self, key: bytes, msg: str) -> bytes:
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def _signing_key(self, date_str: str) -> bytes:
        k_date = self._hmac(("AWS4" + self._secret_key).encode("utf-8"), date_str)
        k_region = self._hmac(k_date, self._region)
        k_service = self._hmac(k_region, self._service)
        return self._hmac(k_service, "aws4_request")

    def sign(
        self,
        method: str,
        host: str,
        path: str,
        query_string: str = "",
        payload: bytes = b"",
    ) -> dict[str, str]:
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y%m%d")
        amz_date = now.strftime("%Y%m%dT%H%M%SZ")

        payload_hash = hashlib.sha256(payload).hexdigest()
        canonical_headers = (
            f"host:{host}\n"
            f"x-amz-content-sha256:{payload_hash}\n"
            f"x-amz-date:{amz_date}\n"
        )
        signed_headers = "host;x-amz-content-sha256;x-amz-date"

        canonical_request = "\n".join([
            method.upper(),
            path or "/",
            query_string,
            canonical_headers,
            signed_headers,
            payload_hash,
        ])

        credential_scope = f"{date_str}/{self._region}/{self._service}/aws4_request"
        string_to_sign = "\n".join([
            "AWS4-HMAC-SHA256",
            amz_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        ])

        signature = hmac.new(
            self._signing_key(date_str),
            string_to_sign.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return {
            "Authorization": (
                f"AWS4-HMAC-SHA256 Credential={self._access_key}/{credential_scope}, "
                f"SignedHeaders={signed_headers}, "
                f"Signature={signature}"
            ),
            "x-amz-date": amz_date,
            "x-amz-content-sha256": payload_hash,
        }
