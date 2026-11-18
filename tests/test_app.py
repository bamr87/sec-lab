import json
import socket
import threading
import urllib.error
import urllib.request
from contextlib import contextmanager

import pytest

import seclab
from seclab.app import check_bind, make_server


def test_loopback_allowed():
    check_bind("127.0.0.1")


def test_public_refused():
    with pytest.raises(SystemExit):
        check_bind("0.0.0.0")


@contextmanager
def running(host):
    server = make_server(host, 0)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def get(url):
    try:
        with urllib.request.urlopen(url) as r:
            return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        try:
            return e.code, e.headers, e.read()
        finally:
            e.close()


def test_routes_ipv4():
    with running("127.0.0.1") as s:
        base = f"http://127.0.0.1:{s.server_address[1]}"
        assert s.address_family == socket.AF_INET
        status, _, body = get(base + "/healthz")
        assert (status, body) == (200, b"ok")
        status, _, body = get(base + "/")
        assert (status, body) == (200, f"sec-lab {seclab.__version__}".encode())
        status, headers, body = get(base + "/version")
        assert status == 200
        assert headers["Content-Type"] == "application/json"
        assert json.loads(body) == {"name": "sec-lab", "version": seclab.__version__}
        status, _, _ = get(base + "/nope")
        assert status == 404


def test_localhost_is_ipv4():
    with running("localhost") as s:
        assert s.address_family == socket.AF_INET


def test_make_server_refuses_public():
    with pytest.raises(SystemExit):
        make_server("0.0.0.0", 0)


@pytest.mark.skipif(not socket.has_ipv6, reason="no IPv6 support")
def test_ipv6_loopback_roundtrip():
    with running("::1") as s:
        assert s.address_family == socket.AF_INET6
        status, _, body = get(f"http://[::1]:{s.server_address[1]}/healthz")
        assert (status, body) == (200, b"ok")
