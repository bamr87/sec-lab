"""sec-lab app. Deliberately vulnerable challenges arrive in later phases; it binds to loopback only."""
import argparse
import ipaddress
import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

from seclab import __version__

LOOPBACK = {"127.0.0.1", "localhost", "::1"}


def check_bind(host: str, allow_public: bool = False) -> None:
    if host not in LOOPBACK and not allow_public:
        raise SystemExit(f"refusing to bind {host}: sec-lab is intentionally vulnerable; loopback only")


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if self.path == "/healthz":
            self._send(200, b"ok", "text/plain; charset=utf-8")
        elif self.path == "/version":
            body = json.dumps({"name": "sec-lab", "version": __version__}).encode()
            self._send(200, body, "application/json")
        elif self.path == "/":
            self._send(200, f"sec-lab {__version__}".encode(), "text/plain; charset=utf-8")
        else:
            self._send(404, b"not found", "text/plain; charset=utf-8")


class HTTPServerV6(HTTPServer):
    address_family = socket.AF_INET6


def _is_ipv6(host: str) -> bool:
    try:
        return ipaddress.ip_address(host).version == 6
    except ValueError:
        return False


def make_server(host: str, port: int, allow_public: bool = False) -> HTTPServer:
    """Build the server after the bind guard; IPv6 literals get an AF_INET6 socket."""
    check_bind(host, allow_public)
    cls = HTTPServerV6 if _is_ipv6(host) else HTTPServer
    return cls((host, port), Handler)


def _port(value: str) -> int:
    """argparse type: an integer TCP port in 1-65535 (bad values exit 2 via argparse)."""
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid port {value!r}: not an integer") from None
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError(f"invalid port {port}: must be 1-65535")
    return port


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sec-lab",
        description="Serve the deliberately vulnerable sec-lab app (loopback only by default).",
    )
    parser.add_argument("--host", default="127.0.0.1", help="address to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=_port, default=8000, help="TCP port, 1-65535 (default: 8000)")
    parser.add_argument(
        "--allow-public",
        action="store_true",
        help="permit a non-loopback --host; the app is intentionally vulnerable, so only on an isolated network",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    make_server(args.host, args.port, allow_public=args.allow_public).serve_forever()


if __name__ == "__main__":
    main()
