import pytest

from seclab.app import check_bind


def test_loopback_allowed():
    check_bind("127.0.0.1")


def test_public_refused():
    with pytest.raises(SystemExit):
        check_bind("0.0.0.0")
