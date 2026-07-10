from __future__ import annotations

import xml.etree.ElementTree as ET
from types import TracebackType
from typing import Any, NoReturn
from urllib.parse import urlencode

import httpx

from ncp_api.auth import HmacSigner
from ncp_api.auth_aws import AwsSigV4Signer
from ncp_api.environment import NcpEnv
from ncp_api.exceptions import NcpApiError, NcpAuthError, NcpNetworkError

_S3_NS = "http://s3.amazonaws.com/doc/2006-03-01/"

OBJECT_STORAGE_BASE_URLS: dict[NcpEnv, str] = {
    NcpEnv.PUBLIC: "https://kr.object.ncloudstorage.com",
    NcpEnv.GOV: "https://kr.object.gov-ncloudstorage.com",
    NcpEnv.FIN: "https://kr.object.fin-ncloudstorage.com",
}


class ObjectStorageApi:
    """NCP Object Storage adapter (S3-compatible, AWS SigV4 auth, XML responses)."""

    def __init__(self, base_url: str, signer: HmacSigner) -> None:
        self._base_url = base_url.rstrip("/")
        self._host = httpx.URL(base_url).host
        self._signer = AwsSigV4Signer(signer.access_key, signer.secret_key)
        self._client = httpx.Client()
        self._async_client = httpx.AsyncClient()

    def _auth_headers(self, method: str, path: str, query_string: str = "") -> dict[str, str]:
        return self._signer.sign(method, self._host, path, query_string)

    def _parse_error(self, response: httpx.Response) -> NoReturn:
        code = str(response.status_code)
        message = response.text
        try:
            root = ET.fromstring(response.text)
            code = root.findtext("Code") or root.findtext(f"{{{_S3_NS}}}Code") or code
            message = root.findtext("Message") or root.findtext(f"{{{_S3_NS}}}Message") or message
        except ET.ParseError:
            pass
        if response.status_code in (401, 403):
            raise NcpAuthError(message, error_code=code)
        raise NcpApiError(status_code=response.status_code, error_code=code, message=message)

    def _handle_response(self, response: httpx.Response) -> ET.Element:
        if response.is_error:
            self._parse_error(response)
        return ET.fromstring(response.text)

    def _ns(self, tag: str) -> str:
        return f"{{{_S3_NS}}}{tag}"

    def _text(self, el: ET.Element, tag: str) -> str:
        return el.findtext(self._ns(tag)) or el.findtext(tag) or ""

    def _parse_list_buckets(self, root: ET.Element) -> dict[str, Any]:
        owner: dict[str, str] = {}
        owner_el = root.find(self._ns("Owner"))
        if owner_el is not None:
            owner = {
                "id": self._text(owner_el, "ID"),
                "displayName": self._text(owner_el, "DisplayName"),
            }

        buckets: list[dict[str, str]] = []
        buckets_el = root.find(self._ns("Buckets"))
        if buckets_el is not None:
            for b in buckets_el.findall(self._ns("Bucket")):
                buckets.append({
                    "name": self._text(b, "Name"),
                    "creationDate": self._text(b, "CreationDate"),
                })

        return {"owner": owner, "buckets": buckets}

    def _build_object_query(
        self,
        prefix: str | None,
        delimiter: str | None,
        encoding_type: str | None,
        max_keys: int | None,
        marker: str | None,
    ) -> str:
        params: dict[str, str] = {}
        if delimiter is not None:
            params["delimiter"] = delimiter
        if encoding_type is not None:
            params["encoding-type"] = encoding_type
        if marker is not None:
            params["marker"] = marker
        if max_keys is not None:
            params["max-keys"] = str(max_keys)
        if prefix is not None:
            params["prefix"] = prefix
        return urlencode(sorted(params.items()))

    def _parse_list_objects(self, root: ET.Element) -> dict[str, Any]:
        is_truncated_text = self._text(root, "IsTruncated").lower()
        contents: list[dict[str, Any]] = []
        for obj in root.findall(self._ns("Contents")):
            owner_el = obj.find(self._ns("Owner"))
            owner: dict[str, str] = {}
            if owner_el is not None:
                owner = {
                    "id": self._text(owner_el, "ID"),
                    "displayName": self._text(owner_el, "DisplayName"),
                }
            size_text = self._text(obj, "Size")
            contents.append({
                "key": self._text(obj, "Key"),
                "lastModified": self._text(obj, "LastModified"),
                "eTag": self._text(obj, "ETag"),
                "size": int(size_text) if size_text else 0,
                "storageClass": self._text(obj, "StorageClass"),
                "owner": owner,
            })

        common_prefixes = [
            self._text(cp, "Prefix")
            for cp in root.findall(self._ns("CommonPrefixes"))
        ]

        max_keys_text = self._text(root, "MaxKeys")
        return {
            "name": self._text(root, "Name"),
            "prefix": self._text(root, "Prefix"),
            "marker": self._text(root, "Marker"),
            "maxKeys": int(max_keys_text) if max_keys_text else 0,
            "delimiter": self._text(root, "Delimiter"),
            "isTruncated": is_truncated_text == "true",
            "contents": contents,
            "commonPrefixes": [p for p in common_prefixes if p],
        }

    def list_objects(
        self,
        bucket: str,
        *,
        prefix: str | None = None,
        delimiter: str | None = None,
        encoding_type: str | None = None,
        max_keys: int | None = None,
        marker: str | None = None,
    ) -> dict[str, Any]:
        path = f"/{bucket}"
        query_string = self._build_object_query(prefix, delimiter, encoding_type, max_keys, marker)
        url = f"{self._base_url}{path}?{query_string}" if query_string else f"{self._base_url}{path}"
        headers = self._auth_headers("GET", path, query_string)
        try:
            response = self._client.get(url, headers=headers)
            root = self._handle_response(response)
        except (NcpAuthError, NcpApiError):
            raise
        except httpx.ConnectError as exc:
            raise NcpNetworkError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise NcpNetworkError(str(exc)) from exc
        return self._parse_list_objects(root)

    async def alist_objects(
        self,
        bucket: str,
        *,
        prefix: str | None = None,
        delimiter: str | None = None,
        encoding_type: str | None = None,
        max_keys: int | None = None,
        marker: str | None = None,
    ) -> dict[str, Any]:
        path = f"/{bucket}"
        query_string = self._build_object_query(prefix, delimiter, encoding_type, max_keys, marker)
        url = f"{self._base_url}{path}?{query_string}" if query_string else f"{self._base_url}{path}"
        headers = self._auth_headers("GET", path, query_string)
        try:
            response = await self._async_client.get(url, headers=headers)
            root = self._handle_response(response)
        except (NcpAuthError, NcpApiError):
            raise
        except httpx.ConnectError as exc:
            raise NcpNetworkError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise NcpNetworkError(str(exc)) from exc
        return self._parse_list_objects(root)

    def list_buckets(self) -> dict[str, Any]:
        headers = self._auth_headers("GET", "/")
        try:
            response = self._client.get(f"{self._base_url}/", headers=headers)
            root = self._handle_response(response)
        except (NcpAuthError, NcpApiError):
            raise
        except httpx.ConnectError as exc:
            raise NcpNetworkError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise NcpNetworkError(str(exc)) from exc
        return self._parse_list_buckets(root)

    async def alist_buckets(self) -> dict[str, Any]:
        headers = self._auth_headers("GET", "/")
        try:
            response = await self._async_client.get(f"{self._base_url}/", headers=headers)
            root = self._handle_response(response)
        except (NcpAuthError, NcpApiError):
            raise
        except httpx.ConnectError as exc:
            raise NcpNetworkError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise NcpNetworkError(str(exc)) from exc
        return self._parse_list_buckets(root)

    def close(self) -> None:
        self._client.close()

    async def aclose(self) -> None:
        await self._async_client.aclose()

    def __enter__(self) -> ObjectStorageApi:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    async def __aenter__(self) -> ObjectStorageApi:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()
