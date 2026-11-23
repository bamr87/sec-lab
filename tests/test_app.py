import json
import socket
import threading
import urllib.error
import urllib.request
from contextlib import contextmanager

import pytest

import seclab
from seclab import app
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


# --- CLI (SECL-002): the loopback guard is reachable from the command line ---


def test_help_exits_zero_without_binding(capsys, monkeypatch):
    def no_bind(*a, **k):
        raise AssertionError("--help must not build a server")

    monkeypatch.setattr(app, "make_server", no_bind)
    with pytest.raises(SystemExit) as exc:
        app.main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    for flag in ("--host", "--port", "--allow-public"):
        assert flag in out


def test_parse_args_defaults():
    args = app.parse_args([])
    assert (args.host, args.port, args.allow_public) == ("127.0.0.1", 8000, False)


@pytest.mark.parametrize("bad", ["0", "70000", "abc"])
def test_bad_port_is_usage_error(bad):
    with pytest.raises(SystemExit) as exc:
        app.parse_args(["--port", bad])
    assert exc.value.code == 2


def test_cli_public_host_refused():
    with pytest.raises(SystemExit) as exc:
        app.main(["--host", "0.0.0.0"])
    assert exc.value.code not in (0, None)
    assert "refusing to bind 0.0.0.0" in str(exc.value.code)


def test_cli_allow_public_binds():
    args = app.parse_args(["--host", "0.0.0.0", "--allow-public"])
    assert args.allow_public is True
    server = make_server(args.host, 0, allow_public=args.allow_public)
    try:
        assert server.server_address[1] != 0
    finally:
        server.server_close()


def test_main_passes_flags_to_make_server(monkeypatch):
    seen = {}

    class Fake:
        server_address = ("0.0.0.0", 9001)

        def serve_forever(self):
            seen["served"] = True

        def server_close(self):
            seen["closed"] = True

    def fake_make_server(host, port, allow_public=False):
        seen.update(host=host, port=port, allow_public=allow_public)
        return Fake()

    monkeypatch.setattr(app, "make_server", fake_make_server)
    app.main(["--host", "0.0.0.0", "--port", "9001", "--allow-public"])
    assert seen == {"host": "0.0.0.0", "port": 9001, "allow_public": True, "served": True, "closed": True}


def test_main_reports_address_and_stops_cleanly_on_ctrl_c(capsys, monkeypatch):
    real = app.make_server
    built = {}

    def interrupted_server(host, port, allow_public=False):
        server = real(host, 0, allow_public)  # port 0: a real loopback socket, no fixed port

        def stop():
            raise KeyboardInterrupt

        server.serve_forever = stop
        built["server"] = server
        return server

    monkeypatch.setattr(app, "make_server", interrupted_server)
    app.main([])  # returns normally: KeyboardInterrupt is a clean exit (status 0)
    port = built["server"].server_address[1]
    assert f"listening on http://127.0.0.1:{port}" in capsys.readouterr().err
    assert built["server"].socket.fileno() == -1  # server_close() released the socket
