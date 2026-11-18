<!-- kit: governance v0.1.0 -->
# 0002 — Missions

- **Status:** proposed
- **Date:** 2026-11-16
- **Proposed by:** Grok Bot (agent), at the maintainer's request
- **Ratified by:**
- **Affects:** constitution §1; PRD §1.1; feature SECL-008
- **Supersedes:** none
- **Related:** [PRD.md](../../PRD.md) §1.1; feature SECL-008

## Context

Constitution §1 Mission was a product description (or, for a new constitution, had not been written yet), not a three-mission direction statement. The fleet now requires every repo's constitution §1 to be one direction statement followed by exactly three numbered missions, adopted through a numbered amendment the maintainer ratifies by merging. The maintainer asked for those missions to be comprehensive and epic: Sec Lab as the ultimate open home for all things hands-on application-security practice. Mission 1 follows the maintainer's wording, adapted to this domain: provide data, tools, resources and transparency for all stakeholders, domain practitioners and the general public. The ambition is the direction, not a claim that the work is already finished. The missions are aligned with this repo's existing constitution and PRD.

## Amendment

Replace constitution §1 with the following, retitled **Missions**:

Sec Lab's direction is to become the ultimate open home for all things hands-on application-security practice — data, tools, resources and transparency, gathered in one place that anyone can inspect and reuse.

1. **Provide data, tools, resources and transparency for all stakeholders, security practitioners and students, and the general public.** Learners, reviewers and anyone practicing defensive security are first-class audiences. The aim is a shared, inspectable commons: the same practice app, the same scanners, and the same fix write-ups for everyone.
2. **Teach people to find and fix vulnerabilities in a deliberately broken app, with SAST and DAST scanners and write-ups for each fix, for local use only.** The lab exists so practice happens on purpose, in an isolated tree, never against a production system or a third party.
3. **Feed the patterns learned here back into fleet hardening — identity, edge and hub security — so practice in the lab improves real defenses.** What is discovered and fixed in the lab should become reusable guidance, not a private notebook.

These missions set the course; they do not claim the work is finished. They serve the PRD's learning-first path: an intentionally vulnerable app, Semgrep, Bandit and ZAP, and write-ups that can inform fleet hardening, always for local use only.

_Source: [PRD.md](../PRD.md) §1.1._


## Consequences

Agents and reviewers judge fit against these three missions before inventing scope, treating them as the direction of the repo rather than a description of what already ships. The same text is added as PRD §1.1 so the constitution's `_Source:` line stays accurate. The original PRD purpose / overview paragraph is left in place. This PR also aligns the README and AGENTS.md taglines with the missions and links them to constitution §1, and adds feature SECL-008 to the feature catalog, traced to requirement MR1. Merging this PR ratifies amendment 0002. Until then the record stays `Status: proposed`.
