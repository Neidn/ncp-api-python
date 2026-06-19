import ncp_api


def test_version_exists():
    assert isinstance(ncp_api.__version__, str)


def test_version_format():
    parts = ncp_api.__version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
