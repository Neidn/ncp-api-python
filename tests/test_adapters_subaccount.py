from __future__ import annotations

from typing import Any

from ncp_api.adapters.subaccount import SubAccountApi

BASE_URL = "https://subaccount.apigw.ntruss.com"

SAMPLE_RESPONSE = {
    "page": 0,
    "totalPages": 1,
    "totalItems": 1,
    "hasPrevious": False,
    "hasNext": False,
    "items": [
        {
            "subAccountId": "89b556d0-0000-0000-0000-000000000000",
            "subAccountNo": 16000,
            "loginId": "hello",
            "name": "hello",
            "email": "hello@example.com",
            "active": True,
        }
    ],
    "isFirst": True,
    "isLast": True,
}


def make_api() -> SubAccountApi:
    from ncp_api.auth import HmacSigner

    return SubAccountApi(BASE_URL, HmacSigner("testkey", "testsecret"))


def test_get_sub_accounts_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    result = make_api().get_sub_accounts()
    assert isinstance(result, dict)
    assert result["totalItems"] == 1
    assert result["items"][0]["loginId"] == "hello"


def test_get_sub_accounts_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_sub_accounts()
    sent = httpx_mock.get_requests()[0]
    assert "/api/v1/sub-accounts" in str(sent.url)


def test_get_sub_accounts_with_filters(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_sub_accounts(
        search_column="loginId", search_word="hello", page=1, size=20
    )
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "searchColumn=loginId" in url
    assert "searchWord=hello" in url
    assert "page=1" in url
    assert "size=20" in url


def test_get_sub_accounts_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    make_api().get_sub_accounts()
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers


async def test_aget_sub_accounts_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=SAMPLE_RESPONSE)
    result = await make_api().aget_sub_accounts()
    assert isinstance(result, dict)
    assert result["items"][0]["subAccountId"] == "89b556d0-0000-0000-0000-000000000000"
