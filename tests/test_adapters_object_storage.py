from __future__ import annotations

from typing import Any

import pytest

from ncp_api.adapters.object_storage import ObjectStorageApi
from ncp_api.exceptions import NcpApiError, NcpAuthError

BASE_URL = "https://kr.object.ncloudstorage.com"

SAMPLE_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Owner>
    <ID>user123</ID>
    <DisplayName>testuser</DisplayName>
  </Owner>
  <Buckets>
    <Bucket>
      <Name>my-bucket</Name>
      <CreationDate>2024-01-15T10:30:00.000Z</CreationDate>
    </Bucket>
    <Bucket>
      <Name>another-bucket</Name>
      <CreationDate>2024-03-01T08:00:00.000Z</CreationDate>
    </Bucket>
  </Buckets>
</ListAllMyBucketsResult>
"""

EMPTY_BUCKETS_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Owner>
    <ID>user123</ID>
    <DisplayName>testuser</DisplayName>
  </Owner>
  <Buckets/>
</ListAllMyBucketsResult>
"""

ERROR_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<Error>
  <Code>AccessDenied</Code>
  <Message>Access Denied</Message>
</Error>
"""


def make_api() -> ObjectStorageApi:
    from ncp_api.auth import HmacSigner

    return ObjectStorageApi(BASE_URL, HmacSigner("testkey", "testsecret"))


def test_list_buckets_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_XML, headers={"Content-Type": "application/xml"}
    )
    result = make_api().list_buckets()
    assert isinstance(result, dict)
    assert "owner" in result
    assert "buckets" in result


def test_list_buckets_owner_fields(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_XML, headers={"Content-Type": "application/xml"}
    )
    result = make_api().list_buckets()
    assert result["owner"]["id"] == "user123"
    assert result["owner"]["displayName"] == "testuser"


def test_list_buckets_bucket_list(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_XML, headers={"Content-Type": "application/xml"}
    )
    result = make_api().list_buckets()
    assert len(result["buckets"]) == 2
    assert result["buckets"][0]["name"] == "my-bucket"
    assert result["buckets"][0]["creationDate"] == "2024-01-15T10:30:00.000Z"
    assert result["buckets"][1]["name"] == "another-bucket"


def test_list_buckets_correct_url(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_XML, headers={"Content-Type": "application/xml"}
    )
    make_api().list_buckets()
    sent = httpx_mock.get_requests()[0]
    assert sent.method == "GET"
    assert "kr.object.ncloudstorage.com" in str(sent.url)


def test_list_buckets_aws_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_XML, headers={"Content-Type": "application/xml"}
    )
    make_api().list_buckets()
    sent = httpx_mock.get_requests()[0]
    assert "Authorization" in sent.headers
    assert sent.headers["Authorization"].startswith("AWS4-HMAC-SHA256")
    assert "x-amz-date" in sent.headers
    assert "x-amz-content-sha256" in sent.headers


def test_list_buckets_auth_contains_credential(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_XML, headers={"Content-Type": "application/xml"}
    )
    make_api().list_buckets()
    sent = httpx_mock.get_requests()[0]
    auth = sent.headers["Authorization"]
    assert "Credential=testkey/" in auth
    assert "kr-standard/s3/aws4_request" in auth
    assert "SignedHeaders=host;x-amz-content-sha256;x-amz-date" in auth


def test_list_buckets_empty(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=EMPTY_BUCKETS_XML, headers={"Content-Type": "application/xml"}
    )
    result = make_api().list_buckets()
    assert result["buckets"] == []
    assert result["owner"]["id"] == "user123"


def test_list_buckets_403_raises_auth_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(status_code=403, text=ERROR_XML)
    with pytest.raises(NcpAuthError):
        make_api().list_buckets()


def test_list_buckets_error_xml_parsed(httpx_mock: Any) -> None:
    httpx_mock.add_response(status_code=403, text=ERROR_XML)
    with pytest.raises(NcpAuthError) as exc_info:
        make_api().list_buckets()
    assert exc_info.value.error_code == "AccessDenied"


def test_list_buckets_500_raises_api_error(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        status_code=500,
        text="<Error><Code>InternalError</Code><Message>Internal Server Error</Message></Error>",
    )
    with pytest.raises(NcpApiError):
        make_api().list_buckets()


@pytest.mark.asyncio
async def test_alist_buckets_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_XML, headers={"Content-Type": "application/xml"}
    )
    result = await make_api().alist_buckets()
    assert isinstance(result, dict)
    assert len(result["buckets"]) == 2
    assert result["buckets"][0]["name"] == "my-bucket"


# --- list_objects ---

SAMPLE_OBJECTS_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Name>my-bucket</Name>
  <Prefix></Prefix>
  <Marker></Marker>
  <MaxKeys>1000</MaxKeys>
  <IsTruncated>false</IsTruncated>
  <Contents>
    <Key>file1.txt</Key>
    <LastModified>2024-01-15T10:30:00.000Z</LastModified>
    <ETag>&quot;abc123&quot;</ETag>
    <Size>1024</Size>
    <Owner>
      <ID>user123</ID>
      <DisplayName>testuser</DisplayName>
    </Owner>
    <StorageClass>STANDARD</StorageClass>
  </Contents>
  <Contents>
    <Key>subdir/file2.txt</Key>
    <LastModified>2024-02-01T08:00:00.000Z</LastModified>
    <ETag>&quot;def456&quot;</ETag>
    <Size>2048</Size>
    <Owner>
      <ID>user123</ID>
      <DisplayName>testuser</DisplayName>
    </Owner>
    <StorageClass>STANDARD</StorageClass>
  </Contents>
</ListBucketResult>
"""

SAMPLE_OBJECTS_DELIMITED_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Name>my-bucket</Name>
  <Prefix></Prefix>
  <Marker></Marker>
  <MaxKeys>1000</MaxKeys>
  <Delimiter>/</Delimiter>
  <IsTruncated>false</IsTruncated>
  <Contents>
    <Key>file1.txt</Key>
    <LastModified>2024-01-15T10:30:00.000Z</LastModified>
    <ETag>&quot;abc123&quot;</ETag>
    <Size>1024</Size>
    <StorageClass>STANDARD</StorageClass>
  </Contents>
  <CommonPrefixes>
    <Prefix>subdir/</Prefix>
  </CommonPrefixes>
</ListBucketResult>
"""

TRUNCATED_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Name>my-bucket</Name>
  <Prefix></Prefix>
  <Marker></Marker>
  <MaxKeys>1</MaxKeys>
  <IsTruncated>true</IsTruncated>
  <Contents>
    <Key>file1.txt</Key>
    <LastModified>2024-01-15T10:30:00.000Z</LastModified>
    <ETag>&quot;abc123&quot;</ETag>
    <Size>512</Size>
    <StorageClass>STANDARD</StorageClass>
  </Contents>
</ListBucketResult>
"""


def test_list_objects_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_XML, headers={"Content-Type": "application/xml"}
    )
    result = make_api().list_objects("my-bucket")
    assert isinstance(result, dict)
    assert result["name"] == "my-bucket"


def test_list_objects_contents(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_XML, headers={"Content-Type": "application/xml"}
    )
    result = make_api().list_objects("my-bucket")
    assert len(result["contents"]) == 2
    obj = result["contents"][0]
    assert obj["key"] == "file1.txt"
    assert obj["size"] == 1024
    assert obj["storageClass"] == "STANDARD"
    assert obj["owner"]["id"] == "user123"


def test_list_objects_correct_path(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_XML, headers={"Content-Type": "application/xml"}
    )
    make_api().list_objects("my-bucket")
    sent = httpx_mock.get_requests()[0]
    assert "/my-bucket" in str(sent.url)


def test_list_objects_prefix_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_XML, headers={"Content-Type": "application/xml"}
    )
    make_api().list_objects("my-bucket", prefix="subdir/")
    sent = httpx_mock.get_requests()[0]
    assert "prefix=subdir" in str(sent.url)


def test_list_objects_max_keys_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_XML, headers={"Content-Type": "application/xml"}
    )
    make_api().list_objects("my-bucket", max_keys=50)
    sent = httpx_mock.get_requests()[0]
    assert "max-keys=50" in str(sent.url)


def test_list_objects_marker_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_XML, headers={"Content-Type": "application/xml"}
    )
    make_api().list_objects("my-bucket", marker="file1.txt")
    sent = httpx_mock.get_requests()[0]
    assert "marker=file1.txt" in str(sent.url)


def test_list_objects_delimiter_param(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_DELIMITED_XML, headers={"Content-Type": "application/xml"}
    )
    make_api().list_objects("my-bucket", delimiter="/")
    sent = httpx_mock.get_requests()[0]
    assert "delimiter=" in str(sent.url)


def test_list_objects_common_prefixes(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_DELIMITED_XML, headers={"Content-Type": "application/xml"}
    )
    result = make_api().list_objects("my-bucket", delimiter="/")
    assert result["commonPrefixes"] == ["subdir/"]
    assert result["delimiter"] == "/"


def test_list_objects_is_truncated_false(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_XML, headers={"Content-Type": "application/xml"}
    )
    result = make_api().list_objects("my-bucket")
    assert result["isTruncated"] is False


def test_list_objects_is_truncated_true(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=TRUNCATED_XML, headers={"Content-Type": "application/xml"}
    )
    result = make_api().list_objects("my-bucket", max_keys=1)
    assert result["isTruncated"] is True
    assert result["maxKeys"] == 1


def test_list_objects_aws_auth_headers(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_XML, headers={"Content-Type": "application/xml"}
    )
    make_api().list_objects("my-bucket")
    sent = httpx_mock.get_requests()[0]
    assert sent.headers["Authorization"].startswith("AWS4-HMAC-SHA256")
    assert "x-amz-date" in sent.headers


@pytest.mark.asyncio
async def test_alist_objects_returns_dict(httpx_mock: Any) -> None:
    httpx_mock.add_response(
        text=SAMPLE_OBJECTS_XML, headers={"Content-Type": "application/xml"}
    )
    result = await make_api().alist_objects("my-bucket", prefix="subdir/")
    assert isinstance(result, dict)
    assert result["name"] == "my-bucket"
