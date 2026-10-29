# sec-lab

> A deliberately vulnerable practice app with SAST/DAST pipelines and CTF-style challenges. Local use only.

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
```

## How it grows

The roadmap lives in [PRD.md](PRD.md) and [features/features.yml](features/features.yml) (ids `SECL-NNN`, most `status: planned`). Work arrives as pull requests from the hub's evolution and fan-out loops, the `@claude` handler, or the local `evolve` lane (off until `EVOLVE_ENABLED=true`). A human merges every PR. Rules: [docs/constitution.md](docs/constitution.md) · agent guide: [AGENTS.md](AGENTS.md).

## License

[MIT](LICENSE)
