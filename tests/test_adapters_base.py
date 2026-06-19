from __future__ import annotations

from typing import Any

import httpx
import pytest

from ncp_api.adapters.base import NcpHttpAdapter
from ncp_api.auth import HmacSigner
from ncp_api.exceptions import NcpApiError, NcpAuthError, NcpNetworkError


def make_adapter(base_url: str = "https://ncloud.apigw.ntruss.com") -> NcpHttpAdapter:
    signer = HmacSigner("testkey", "testsecret")
    return NcpHttpAdapter(base_url, signer)


def test_base_url_uses_env_url_when_no_service_override() -> None:
    adapter = make_adapter("https://example.com")
    assert adapter.base_url == "https://example.com"


def test_service_base_url_override() -> None:
    class ServiceWithOwnDomain(NcpHttpAdapter):
        _service_base_url = "https://kr.object.ncloudstorage.com"

    signer = HmacSigner("k", "s")
    service = ServiceWithOwnDomain("https://ncloud.apigw.ntruss.com", signer)
    assert service.base_url == "https://kr.object.ncloudstorage.com"


def test_path_prefix_default_empty() -> None:
    adapter = make_adapter()
    assert adapter.path_prefix == ""


def test_path_prefix_combined_in_resolve() -> None:
    class ServerApi(NcpHttpAdapter):
        path_prefix = "/vserver/v2"

    signer = HmacSigner("k", "s")
    api = ServerApi("https://ncloud.apigw.ntruss.com", signer)
    assert api._resolve_url("/getServerInstanceList") == (
        "https://ncloud.apigw.ntruss.com/vserver/v2/getServerInstanceList"
    )


def test_request_success(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"returnCode": "0", "data": "ok"})
    adapter = make_adapter()
    result = adapter.request("GET", "/test/path")
    assert result == {"returnCode": "0", "data": "ok"}


def test_request_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={})
    adapter = make_adapter()
    adapter.request("GET", "/test/path")
    sent_request = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent_request.headers
    assert "x-ncp-iam-access-key" in sent_request.headers
    assert "x-ncp-apigw-signature-v2" in sent_request.headers


def test_request_401_raises_auth_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        status_code=401,
        json={"returnCode": "401", "returnMessage": "Unauthorized"},
    )
    adapter = make_adapter()
    with pytest.raises(NcpAuthError):
        adapter.request("GET", "/test/path")


def test_request_4xx_raises_api_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        status_code=400,
        json={"returnCode": "1001", "returnMessage": "Invalid parameter"},
    )
    adapter = make_adapter()
    with pytest.raises(NcpApiError) as exc_info:
        adapter.request("GET", "/test/path")
    assert exc_info.value.status_code == 400
    assert exc_info.value.error_code == "1001"
    assert exc_info.value.message == "Invalid parameter"


def test_request_5xx_raises_api_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        status_code=500,
        json={"returnCode": "9999", "returnMessage": "Internal error"},
    )
    adapter = make_adapter()
    with pytest.raises(NcpApiError) as exc_info:
        adapter.request("GET", "/test/path")
    assert exc_info.value.status_code == 500


def test_request_network_error_raises_network_error(httpx_mock: Any) -> None:
    httpx_mock.add_exception(httpx.ConnectError("connection refused"))
    adapter = make_adapter()
    with pytest.raises(NcpNetworkError):
        adapter.request("GET", "/test/path")


def test_request_timeout_raises_network_error(httpx_mock: Any) -> None:
    httpx_mock.add_exception(httpx.TimeoutException("timed out"))
    adapter = make_adapter()
    with pytest.raises(NcpNetworkError):
        adapter.request("GET", "/test/path")


@pytest.mark.asyncio
async def test_arequest_success(httpx_mock: Any) -> None:
    httpx_mock.add_response(json={"returnCode": "0"})
    adapter = make_adapter()
    result = await adapter.arequest("GET", "/test/path")
    assert result == {"returnCode": "0"}


@pytest.mark.asyncio
async def test_arequest_401_raises_auth_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(status_code=401, json={})
    adapter = make_adapter()
    with pytest.raises(NcpAuthError):
        await adapter.arequest("GET", "/test/path")
