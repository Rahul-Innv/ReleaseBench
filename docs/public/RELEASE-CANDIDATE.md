# ReleaseBench 0.1.0 private release candidate

Status: local `0.1.0` private-pre-public candidate; candidate inactive; all outward actions remain
closed.

## Version decision

- No local tags were observed; ReleaseBench has no shipped version to supersede.
- `.claude-plugin/plugin.json` and `pyproject.toml` both declare `0.1.0`.
- `CHANGELOG.md` consolidates the initial repository, atomic-family extraction, validation, and
  packaging work under the same unshipped `0.1.0` candidate.
- `v0.1.0` is the proposed first tag. The tag does not exist and was not created by this lane.

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
action, package publication, or live promotion is part of this candidate.

## Deliberately not performed

No remote fetch/pull/push, remote mutation, local or remote tag, host Release, visibility or
metadata change, host/API call, registry read, authentication, provider call, public verification,
package publication, skill lifecycle action, archive mutation, or destructive cleanup occurred or is
authorized by this status. Tagging, tag push, host Release, installation, host action, publication,
and public exposure remain separate gates.
