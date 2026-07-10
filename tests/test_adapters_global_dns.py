from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.global_dns import GlobalDnsApi
from ncp_api.exceptions import NcpApiError, NcpAuthError

BASE_URL = "https://globaldns.apigw.ntruss.com"

SAMPLE_DOMAIN_RESPONSE = {
    "content": [
        {
            "id": 1001,
            "name": "example.com",
            "status": "SUCCESS",
            "completeYn": True,
            "dnssecYn": False,
        },
        {
            "id": 1002,
            "name": "test.com",
            "status": "SUCCESS",
            "completeYn": True,
            "dnssecYn": False,
        },
    ],
    "totalElements": 2,
    "totalPages": 1,
    "first": True,
    "last": True,
    "size": 20,
    "number": 0,
    "numberOfElements": 2,
    "empty": False,
}

EMPTY_DOMAIN_RESPONSE = {
    "content": [],
    "totalElements": 0,
    "totalPages": 0,
    "first": True,
    "last": True,
    "size": 20,
    "number": 0,
    "numberOfElements": 0,
    "empty": True,
}

SAMPLE_RECORD_RESPONSE = {
    "content": [
        {"id": 2001, "type": "A", "name": "www", "content": "1.2.3.4", "ttl": 300},
        {
            "id": 2002,
            "type": "CNAME",
            "name": "api",
            "content": "www.example.com",
            "ttl": 300,
        },
        {
            "id": 2003,
            "type": "MX",
            "name": "@",
            "content": "mail.example.com",
            "ttl": 3600,
        },
    ],
    "totalElements": 3,
    "totalPages": 1,
    "first": True,
    "last": True,
    "size": 20,
    "number": 0,
    "numberOfElements": 3,
    "empty": False,
}

EMPTY_RECORD_RESPONSE = {
    "content": [],
    "totalElements": 0,
    "totalPages": 0,
    "first": True,
    "last": True,
    "size": 20,
    "number": 0,
    "numberOfElements": 0,
    "empty": True,
}


def make_api() -> GlobalDnsApi:
    from ncp_api.auth import HmacSigner

    return GlobalDnsApi(BASE_URL, HmacSigner("testkey", "testsecret"))


# --- get_domain_list ---


def test_get_domain_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_DOMAIN_RESPONSE)
    result = make_api().get_domain_list()
    assert isinstance(result, dict)
    assert result["totalElements"] == 2


def test_get_domain_list_content(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_DOMAIN_RESPONSE)
    result = make_api().get_domain_list()
    assert len(result["content"]) == 2
    assert result["content"][0]["name"] == "example.com"
    assert result["content"][1]["id"] == 1002


def test_get_domain_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_DOMAIN_RESPONSE)
    make_api().get_domain_list()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
    assert "/dns/v1/ncpdns/domain" in str(sent.url)


def test_get_domain_list_default_page_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_DOMAIN_RESPONSE)
    make_api().get_domain_list()
    url = str(httpx_mock.get_requests()[0].url)
    assert "page=0" in url
    assert "size=20" in url


def test_get_domain_list_custom_page_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_DOMAIN_RESPONSE)
    make_api().get_domain_list(page=1, size=10)
    url = str(httpx_mock.get_requests()[0].url)
    assert "page=1" in url
    assert "size=10" in url


def test_get_domain_list_domain_name_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_DOMAIN_RESPONSE)
    make_api().get_domain_list(domain_name="example.com")
    assert "domainName=example.com" in str(httpx_mock.get_requests()[0].url)


def test_get_domain_list_empty(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=EMPTY_DOMAIN_RESPONSE)
    result = make_api().get_domain_list()
    assert result["totalElements"] == 0
    assert result["content"] == []
    assert result["empty"] is True


def test_get_domain_list_401_raises_auth_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        status_code=401, json={"returnCode": "401", "returnMessage": "Unauthorized"}
    )
    with pytest.raises(NcpAuthError):
        make_api().get_domain_list()


def test_get_domain_list_500_raises_api_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        status_code=500, json={"returnCode": "500", "returnMessage": "Internal Error"}
    )
    with pytest.raises(NcpApiError):
        make_api().get_domain_list()


def test_get_domain_list_base_url(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_DOMAIN_RESPONSE)
    make_api().get_domain_list()
    sent = httpx_mock.get_requests()[0]
    assert "globaldns.apigw.ntruss.com" in str(sent.url)


async def test_aget_domain_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_DOMAIN_RESPONSE)
    result = await make_api().aget_domain_list()
    assert isinstance(result, dict)
    assert result["content"][0]["name"] == "example.com"


# --- get_record_list ---


def test_get_record_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RECORD_RESPONSE)
    result = make_api().get_record_list(1001)
    assert isinstance(result, dict)
    assert result["totalElements"] == 3


def test_get_record_list_content(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RECORD_RESPONSE)
    result = make_api().get_record_list(1001)
    records = result["content"]
    assert records[0]["type"] == "A"
    assert records[0]["content"] == "1.2.3.4"
    assert records[1]["type"] == "CNAME"


def test_get_record_list_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RECORD_RESPONSE)
    make_api().get_record_list(1001)
    sent = httpx_mock.get_requests()[0]
    assert "/dns/v1/ncpdns/record/1001" in str(sent.url)


def test_get_record_list_record_type_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RECORD_RESPONSE)
    make_api().get_record_list(1001, record_type="A")
    assert "recordType=A" in str(httpx_mock.get_requests()[0].url)


def test_get_record_list_search_content_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RECORD_RESPONSE)
    make_api().get_record_list(1001, search_content="www")
    assert "searchContent=www" in str(httpx_mock.get_requests()[0].url)


def test_get_record_list_pagination_params(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RECORD_RESPONSE)
    make_api().get_record_list(1001, page=2, size=10)
    url = str(httpx_mock.get_requests()[0].url)
    assert "page=2" in url
    assert "size=10" in url


def test_get_record_list_empty(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=EMPTY_RECORD_RESPONSE)
    result = make_api().get_record_list(1001)
    assert result["totalElements"] == 0
    assert result["content"] == []


async def test_aget_record_list_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RECORD_RESPONSE)
    result = await make_api().aget_record_list(1001, record_type="CNAME")
    assert isinstance(result, dict)
    assert len(result["content"]) == 3
