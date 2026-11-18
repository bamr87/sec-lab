"""sec-lab app. Deliberately vulnerable challenges arrive in later phases; it binds to loopback only."""
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


def main(host: str = "127.0.0.1", port: int = 8000) -> None:
    make_server(host, port).serve_forever()


if __name__ == "__main__":
    main()
