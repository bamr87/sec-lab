"""sec-lab app. Deliberately vulnerable challenges arrive in later phases; it binds to loopback only."""
from http.server import BaseHTTPRequestHandler, HTTPServer

LOOPBACK = {"127.0.0.1", "localhost", "::1"}


def check_bind(host: str, allow_public: bool = False) -> None:
    if host not in LOOPBACK and not allow_public:
        raise SystemExit(f"refusing to bind {host}: sec-lab is intentionally vulnerable; loopback only")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        body = b"ok" if self.path == "/healthz" else b"sec-lab 0.1.0"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body)


def main(host: str = "127.0.0.1", port: int = 8000) -> None:
    check_bind(host)
    HTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
