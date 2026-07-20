# ReleaseBench next-release source candidate

Status: the 0.1.0 package is already published on PyPI; current source contains Unreleased changes;
no next release version has been selected; all new outward actions remain owner-gated.

## Version decision

- PyPI records the earliest 0.1.0 distribution upload on 2026-07-18.
- No matching `v0.1.0` Git tag or GitLab Release exists; do not create either retroactively.
- `.claude-plugin/plugin.json` and `pyproject.toml` still declare 0.1.0 while the new changes remain
  under `CHANGELOG.md`'s Unreleased section.
- Before a future release, choose and commit a version strictly greater than 0.1.0 across every
  version surface, then rebuild and verify from that exact commit.

## Candidate contents

- exactly ten canonical atomic skills: one dispatch-only router and nine leaves;
- exactly three internal non-skill primitives;
- a typed deterministic one-leaf-or-no-safe-route contract;
- the preserved 49-case eval corpus under per-leaf case IDs;
- trigger, near-miss, collision, malformed-request, and full-flow fixtures;
- canonical Codex and Claude Code metadata with implicit Codex invocation disabled;
- an installable Python package wrapping the router with identical behavior;
- portable cross-CLI guidance, governance, security, and owner handoff; and
- offline secret/path and closed-action checks.

## Distribution

ReleaseBench is described by `.claude-plugin/plugin.json` for plugin loading and by `pyproject.toml`
as an installable Python package exposing the router module and the `releasebench` console entry
point. Official plugin validation, the deterministic family suite, and an offline package build with
a metadata check are the applicable local package dry runs. No plugin installation, marketplace
action, new package publication, or live promotion is part of this source candidate.

## Deliberately not performed

This source candidate authorizes no merge, tag, tag push, GitLab Release, settings change, package
publication, skill lifecycle action, or public-state mutation. A read-only audit verified existing
GitLab and PyPI state, but that verification grants no outward authority. Future tagging, Release
creation, publication, settings changes, and promotion remain separate owner gates.
