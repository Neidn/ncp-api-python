from __future__ import annotations

from typing import Any

from ncp_api.adapters.subaccount import SubAccountApi, SubAccountApiV2

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


# -- SubAccountApiV2 (IAM v2, Ncloud API standard spec) ----------------------

V2_USER_RESPONSE = {
    "subAccountId": "4e066e50-9c3a-11e7-8a66-1e5021fa7c80",
    "loginId": "myloginid01",
    "name": "hello",
    "email": "user@example.com",
    "groups": [],
    "active": True,
    "deleted": False,
    "createdDateTime": "2024-01-01T00:00:00Z",
    "principalType": "IamUser",
}

V2_LIST_RESPONSE = {
    "subAccounts": [
        {
            "subAccountId": "4e066e50-9c3a-11e7-8a66-1e5021fa7c80",
            "loginId": "myloginid01",
            "name": "hello",
            "consoleAccessible": True,
            "apiGatewayAccessible": False,
            "active": True,
            "createdDateTime": "2024-01-01T00:00:00Z",
            "lastLoginDateTime": "2024-01-01T00:00:00Z",
            "nrn": (
                "nrn:PUB:IAM::25000000:SubAccount/4e066e50-9c3a-11e7-8a66-1e5021fa7c80"
            ),
        }
    ],
    "totalElements": 1,
    "totalPages": 1,
    "pageNo": 0,
    "pageSize": 20,
}


def make_api_v2() -> SubAccountApiV2:
    from ncp_api.auth import HmacSigner

    return SubAccountApiV2(BASE_URL, HmacSigner("testkey", "testsecret"))


def test_get_user_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=V2_USER_RESPONSE)
    result = make_api_v2().get_user(
        sub_account_id="4e066e50-9c3a-11e7-8a66-1e5021fa7c80"
    )
    sent = httpx_mock.get_requests()[0]
    assert "/api/v2/users/4e066e50-9c3a-11e7-8a66-1e5021fa7c80" in str(sent.url)
    assert result["loginId"] == "myloginid01"


async def test_aget_user_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=V2_USER_RESPONSE)
    result = await make_api_v2().aget_user(
        sub_account_id="4e066e50-9c3a-11e7-8a66-1e5021fa7c80"
    )
    assert result["principalType"] == "IamUser"


def test_list_sub_accounts_path_and_query(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=V2_LIST_RESPONSE)
    make_api_v2().list_sub_accounts(page_no=0, page_size=20)
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert "/api/v2/sub-accounts" in url
    assert "pageNo=0" in url
    assert "pageSize=20" in url


def test_list_sub_accounts_sort_repeated_query_key(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=V2_LIST_RESPONSE)
    make_api_v2().list_sub_accounts(sort=["loginId,asc", "name,desc"])
    sent = httpx_mock.get_requests()[0]
    url = str(sent.url)
    assert url.count("sort=") == 2
    assert "sort=loginId%2Casc" in url
    assert "sort=name%2Cdesc" in url


def test_list_sub_accounts_no_params_sends_no_query(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=V2_LIST_RESPONSE)
    make_api_v2().list_sub_accounts()
    sent = httpx_mock.get_requests()[0]
    assert str(sent.url).endswith("/api/v2/sub-accounts")


async def test_alist_sub_accounts_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=V2_LIST_RESPONSE)
    result = await make_api_v2().alist_sub_accounts(page_no=0, page_size=20)
    assert result["subAccounts"][0]["loginId"] == "myloginid01"
    assert result["totalElements"] == 1


def test_get_user_sends_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(json=V2_USER_RESPONSE)
    make_api_v2().get_user(sub_account_id="4e066e50-9c3a-11e7-8a66-1e5021fa7c80")
    sent = httpx_mock.get_requests()[0]
    assert "x-ncp-apigw-timestamp" in sent.headers
    assert "x-ncp-iam-access-key" in sent.headers
    assert "x-ncp-apigw-signature-v2" in sent.headers
