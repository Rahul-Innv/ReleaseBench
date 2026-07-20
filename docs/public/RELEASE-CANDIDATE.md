# ReleaseBench 0.1.1 source candidate

Status: local source preparation for patch version `0.1.1`; PyPI still carries `0.1.0`; no tag,
GitLab Release, or `0.1.1` package publication has occurred; all outward actions remain owner-gated.

## Version decision

- PyPI records the earliest 0.1.0 distribution upload on 2026-07-18.
- No matching `v0.1.0` Git tag or GitLab Release exists; do not create either retroactively.
- `0.1.1` is a PATCH because it packages documentation, audit/scanner, CI-lane, metadata, and
  release-integrity fixes without changing the routing contract or adding a public capability.
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `pyproject.toml`, and
  `src/releasebench/__init__.py` all declare `0.1.1`.
- `CHANGELOG.md` cuts the audited Unreleased work as `0.1.1` on 2026-07-19 and starts a fresh empty
  Unreleased section. It intentionally has no compare link against nonexistent `v0.1.0`.

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
publication, skill lifecycle action, or public-state mutation. After independent acceptance and a
separate owner approval, the proposed release identity is annotated tag `v0.1.1` plus one matching
GitLab Release. Package publication remains a distinct gate. Never create a retroactive `v0.1.0`
tag or Release.
