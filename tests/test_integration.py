"""
Live integration tests — only run when .env provides credentials.

.env (project root):
    NCP_ACCESS_KEY=ncp_iam_...
    NCP_SECRET_KEY=ncp_iam_...
    NCP_ENV=public          # optional, defaults to public

Run all:        uv run pytest tests/test_integration.py -v
Run one:        uv run pytest tests/test_integration.py::test_live_server_list -v
"""
from __future__ import annotations

from ncp_api.client import NcpClient


def test_live_server_list(live_client: NcpClient) -> None:
    result = live_client.server.get_server_instance_list()
    assert "totalRows" in result
    assert isinstance(result["totalRows"], int)


def test_live_mysql_list(live_client: NcpClient) -> None:
    result = live_client.mysql.get_cloud_mysql_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("cloudMysqlInstanceList", []), list)


def test_live_mongodb_list(live_client: NcpClient) -> None:
    result = live_client.mongodb.get_cloud_mongodb_instance_list()
    assert "totalRows" in result
    assert isinstance(result.get("cloudMongoDbInstanceList", []), list)
