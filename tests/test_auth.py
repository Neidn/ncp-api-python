from __future__ import annotations

import base64
import hashlib
import hmac as stdlib_hmac

from ncp_api.auth import HmacSigner


def _expected_signature(
    secret_key: str, method: str, url: str, timestamp: int, access_key: str
) -> str:
    string_to_sign = f"{method} {url}\n{timestamp}\n{access_key}"
    mac = stdlib_hmac.new(
        secret_key.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    )
    return base64.b64encode(mac.digest()).decode("utf-8")


def test_sign_returns_all_three_headers() -> None:
    signer = HmacSigner("testkey", "testsecret")
    headers = signer.sign("GET", "/test/path", 1700000000000)
    assert set(headers.keys()) == {
        "x-ncp-apigw-timestamp",
        "x-ncp-iam-access-key",
        "x-ncp-apigw-signature-v2",
    }


def test_sign_timestamp_header() -> None:
    signer = HmacSigner("testkey", "testsecret")
    headers = signer.sign("GET", "/test/path", 1700000000000)
    assert headers["x-ncp-apigw-timestamp"] == "1700000000000"


def test_sign_access_key_header() -> None:
    signer = HmacSigner("mykey", "mysecret")
    headers = signer.sign("GET", "/test/path", 1700000000000)
    assert headers["x-ncp-iam-access-key"] == "mykey"


def test_sign_signature_matches_hmac_sha256() -> None:
    access_key = "testkey"
    secret_key = "testsecret"
    timestamp = 1700000000000
    method = "GET"
    url = "/vserver/v2/getServerInstanceList"

    signer = HmacSigner(access_key, secret_key)
    headers = signer.sign(method, url, timestamp)

    expected = _expected_signature(secret_key, method, url, timestamp, access_key)
    assert headers["x-ncp-apigw-signature-v2"] == expected


def test_sign_different_methods_produce_different_signatures() -> None:
    signer = HmacSigner("key", "secret")
    get_sig = signer.sign("GET", "/path", 1000)["x-ncp-apigw-signature-v2"]
    post_sig = signer.sign("POST", "/path", 1000)["x-ncp-apigw-signature-v2"]
    assert get_sig != post_sig


def test_sign_different_urls_produce_different_signatures() -> None:
    signer = HmacSigner("key", "secret")
    sig_a = signer.sign("GET", "/path/a", 1000)["x-ncp-apigw-signature-v2"]
    sig_b = signer.sign("GET", "/path/b", 1000)["x-ncp-apigw-signature-v2"]
    assert sig_a != sig_b


def test_sign_query_string_included_in_signature() -> None:
    signer = HmacSigner("key", "secret")
    sig_no_query = signer.sign("GET", "/path", 1000)["x-ncp-apigw-signature-v2"]
    sig_with_query = signer.sign("GET", "/path?foo=bar", 1000)[
        "x-ncp-apigw-signature-v2"
    ]
    assert sig_no_query != sig_with_query
