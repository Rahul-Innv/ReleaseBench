---
name: releasebench-publish-repository
description: >-
  Owns the repository-host publication handoff: resolving host identity, preparing remote-project
  creation and first-push instructions when needed, proposing description/topics/avatar/visibility
  changes, and defining post-public verification. Use for first-host, first-push, visibility,
  metadata, avatar, or host-verification requests. In this private candidate it emits a closed-gate
  owner handoff only; it never contacts a host, creates or changes a remote, pushes, changes host
  state, authenticates, or performs network verification.
---

!`node "${CLAUDE_SKILL_DIR}/scripts/read-lessons.mjs" 2>/dev/null || cat "${CLAUDE_SKILL_DIR}/LESSONS.md" 2>/dev/null`

# Prepare the repository-host handoff

Produce one exact, owner-executable host handoff while preserving every outward gate.

## Procedure

1. Read local Git configuration and evidence only. Resolve the intended host, canonical owner/name,
   default branch, whether a remote exists, and whether first host + first push are still required.
   Never infer a deferred project URL.
2. If no remote exists, prepare—but do not run—the project-creation and `git remote add` / first-push
   steps. This leaf is the sole owner of that responsibility; `releasebench-route` only dispatches.
3. Prepare exact proposed description, topics, avatar path, and visibility choice. Keep owner-only
   commands templated with `<TOKEN>`; never request a pasted secret.
4. Prepare verification for visibility, metadata, Releases, CI, and README assets, but do not run
   authenticated or unauthenticated network reads in the current private lane.
5. Emit one `releasebench.publish-handoff/v1` separating verified local facts, deferred owner choices,
   exact outward commands, and the new approvals each command requires.

Detailed host command shapes remain in `references/host-metadata-commands.md`. They are reference
material, not authorization to execute them.

## Non-goals and gates

- Do not edit README content (`releasebench-showcase-readme`) or prepare a version
  (`releasebench-release-version`).
- Do not create or change a remote, create a host project, fetch, pull, push, or first-push.
- Do not change visibility, description, topics, avatar, Releases, or other host metadata.
- Do not call any host API, remote asset URL, provider, browser, registry, or authenticated service.
- Do not claim host state verified from local configuration.

## Feedback loop

Propose reviewable changes to `LESSONS.md`; never silently edit it during a host handoff.

## Bundled files

- `references/host-metadata-commands.md` - gated GitLab/GitHub command shapes.
- `evals/evals.json` - four preserved source eval cases under the canonical ID.
- `scripts/read-lessons.mjs` - internal lesson-reader copy.
