# sec-lab

> Sec Lab's direction is to become the ultimate open home for all things hands-on application-security practice: data, tools, resources and transparency, with a local-only deliberately vulnerable app, scanners and fix write-ups for everyone ([constitution](docs/constitution.md) §1).

Break things on purpose: an intentionally vulnerable web app, the scanners that find the bugs (Semgrep, Bandit, ZAP), and write-ups for each fix.

**Status:** foundation (phase 1). Part of the [bamr87 fleet](https://github.com/bamr87/bamr87).

## Goals

- Intentionally vulnerable app covering OWASP Top 10 classes, run only on localhost
- SAST (Semgrep/Bandit) and DAST (OWASP ZAP) pipelines with reports
- CTF challenge set with flags and fix write-ups

## Skills learned

- Application security (OWASP Top 10)
- Static and dynamic analysis tooling
- Secure coding and remediation
- Threat modeling

## Fleet tie-in

Security patterns learned here feed fleet hardening (zer0-id, edge-gateway, hub security kit).

## Quick start

```bash
pip install -e .[dev] && pytest
python -m seclab.app   # serves on 127.0.0.1:8000 (loopback only)
python -m seclab.app --port 9000   # another port (1-65535); `sec-lab --port 9000` once installed
sec-lab --help         # --host, --port, --allow-public
curl http://127.0.0.1:8000/healthz   # ok
curl http://127.0.0.1:8000/version   # {"name": "sec-lab", "version": "..."}
```

Routes: `/` (banner), `/healthz`, `/version` (JSON); any other path returns 404.

A non-loopback `--host` (e.g. `0.0.0.0`) is refused with `refusing to bind …` unless you also pass `--allow-public`. The app is deliberately vulnerable: only do that on an isolated network.

## How it grows

The roadmap lives in [PRD.md](PRD.md) and [features/features.yml](features/features.yml) (ids `SECL-NNN`, most `status: planned`). Work arrives as pull requests from the hub's evolution and fan-out loops, the `@claude` handler, or the local `evolve` lane (off until `EVOLVE_ENABLED=true`). A human merges every PR. Documentation index: [docs/](docs/README.md). Rules: [docs/constitution.md](docs/constitution.md) · agent guide: [AGENTS.md](AGENTS.md).

## License

[MIT](LICENSE)
