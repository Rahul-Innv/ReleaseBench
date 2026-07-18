---
name: releasebench-route
description: >-
  Routes a broad repository launch, open-source readiness, private pre-public, or "what should
  ReleaseBench do next?" request to exactly one canonical ReleaseBench leaf, or returns no safe route
  when the intent or evidence is ambiguous. Use for the whole ReleaseBench flow and family-level
  routing. Direct single-concern requests should use the matching leaf. This router selects only; it
  never audits, edits, releases, publishes, contacts a host or registry, or duplicates leaf procedures.
---

!`node "${CLAUDE_SKILL_DIR}/scripts/read-lessons.mjs" 2>/dev/null || cat "${CLAUDE_SKILL_DIR}/LESSONS.md" 2>/dev/null`

# Route one ReleaseBench step

Select exactly one next ReleaseBench leaf and stop. Do not perform the selected leaf's work.

## Procedure

1. Resolve the target repository and the user's immediate requested outcome without writing to it.
2. If the user asks for one concern, select its sole owner from the table below.
3. If the user asks for the full private-to-launch flow, select only the first incomplete applicable
   stage: prepare repository, showcase README, prepare release, prepare host handoff, then prepare a
   package when a package channel genuinely applies.
4. If two direct concerns are equally explicit, required evidence is missing, a dependency is not
   accepted, or a lifecycle state is ineligible, return `NO_SAFE_ROUTE` with the exact conflict.
5. Emit one `releasebench.route-receipt/v1` containing the selected leaf or null, evidence, skipped or
   completed stages, authority state, and all closed outward actions.

Use the repository entrypoint `../../src/releasebench/router.py` when a typed deterministic request
is available. Its output is a receipt, not execution.

## Atomic owners

| User outcome | Select |
|---|---|
| Complete local repository preparation | `releasebench-prepare-repository` |
| Read-only repository health gaps | `releasebench-audit-repository` |
| Redacted secret-hygiene findings | `releasebench-scan-secrets` |
| Missing governance-file diffs | `releasebench-scaffold-governance` |
| Truthful README storefront | `releasebench-showcase-readme` |
| Owner-gated host/first-push handoff | `releasebench-publish-repository` |
| Local version/release preparation | `releasebench-release-version` |
| Offline package preparation and dry run | `releasebench-prepare-package` |
| Aligned config schema, validator, and docs | `releasebench-document-config` |

## Non-goals and gates

- Do not inline any leaf procedure or select more than one next leaf.
- Do not silently choose between colliding explicit intents.
- Do not install, enable, expose, activate, promote, supersede, archive, or delete a skill.
- Do not create or change remotes; fetch, pull, push, tag, release, publish, authenticate, call a
  provider or registry, change host state, or perform network verification.
- Keep this private candidate `candidate-inactive` until the owner gates separately change.

## Feedback loop

Propose reviewable changes to `LESSONS.md`; never silently edit lessons during a routed task.

## Bundled files

- `scripts/read-lessons.mjs` - internal lesson-reader copy.
- `evals/evals.json` - five preserved eval cases under the canonical ID.
- `BACKLOG.md` - family backlog; not an execution authority.
- `AGENTS.md` - portable guide owned by the internal ReleaseBench guide primitive.
