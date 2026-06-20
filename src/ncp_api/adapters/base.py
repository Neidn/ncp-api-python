from __future__ import annotations

import time
from types import TracebackType
from typing import Any, ClassVar

import httpx

from ncp_api.auth import HmacSigner
from ncp_api.exceptions import NcpApiError, NcpAuthError, NcpNetworkError, NcpRateLimitError


class NcpHttpAdapter:
    path_prefix: ClassVar[str] = ""
    _service_base_url: ClassVar[str | None] = None

    def __init__(self, env_base_url: str, signer: HmacSigner) -> None:
        self._env_base_url = env_base_url
        self._signer = signer
        self._client = httpx.Client()
        self._async_client = httpx.AsyncClient()

    @property
    def base_url(self) -> str:
        return self._service_base_url or self._env_base_url

    def _resolve_url(self, path: str) -> str:
        return f"{self.base_url}{self.path_prefix}{path}"

    def _make_auth_headers(self, method: str, url: str) -> dict[str, str]:
        parsed = httpx.URL(url)
        sign_target = parsed.path
        if parsed.query:
            sign_target = f"{parsed.path}?{parsed.query.decode('utf-8')}"
        timestamp = int(time.time() * 1000)
        return self._signer.sign(method.upper(), sign_target, timestamp)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        if response.is_error:
            try:
                body: dict[str, Any] = response.json()
            except Exception:
                body = {}
            error_code = str(
                body.get("returnCode", body.get("errorCode", str(response.status_code)))
            )
            message = str(
                body.get("returnMessage", body.get("message", response.text))
            )
            if response.status_code == 401:
                raise NcpAuthError(message, error_code=error_code)
            if response.status_code == 429:
                raise NcpRateLimitError(
                    status_code=response.status_code,
                    error_code=error_code,
                    message=message,
                )
            raise NcpApiError(
                status_code=response.status_code,
                error_code=error_code,
                message=message,
            )
        result: dict[str, Any] = response.json()
        return result

    def request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._resolve_url(path)
        auth_headers = self._make_auth_headers(method, url)
        try:
            response = self._client.request(
                method=method.upper(),
                url=url,
                headers=auth_headers,
                **kwargs,
            )
            return self._handle_response(response)
        except (NcpAuthError, NcpApiError):
            raise
        except httpx.ConnectError as exc:
            raise NcpNetworkError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise NcpNetworkError(str(exc)) from exc

    async def arequest(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._resolve_url(path)
        auth_headers = self._make_auth_headers(method, url)
        try:
            response = await self._async_client.request(
                method=method.upper(),
                url=url,
                headers=auth_headers,
                **kwargs,
            )
            return self._handle_response(response)
        except (NcpAuthError, NcpApiError):
            raise
        except httpx.ConnectError as exc:
            raise NcpNetworkError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise NcpNetworkError(str(exc)) from exc

    def close(self) -> None:
        self._client.close()

    async def aclose(self) -> None:
        await self._async_client.aclose()

    def __enter__(self) -> NcpHttpAdapter:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    async def __aenter__(self) -> NcpHttpAdapter:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()
