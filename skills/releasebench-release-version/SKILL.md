---
name: releasebench-release-version
description: >-
  Prepares one repository version release locally by checking tags and commits already present,
  selecting the next semver, reconciling CHANGELOG and version metadata, and drafting tag and host
  Release instructions. Use for release cuts, version bumps, changelog cuts, tags, or Releases. In
  this private candidate it stops after reviewable local preparation; it never creates a local tag,
  pushes, contacts a host, creates or backfills a Release, or publishes a package.
---

!`node "${CLAUDE_SKILL_DIR}/scripts/read-lessons.mjs" 2>/dev/null || cat "${CLAUDE_SKILL_DIR}/LESSONS.md" 2>/dev/null`

# Prepare a versioned release locally

Produce one internally consistent local release-preparation receipt. Do not create release state.

## Procedure

1. Read the local CHANGELOG, version metadata, existing local tags, and commits since the last tag.
   An empty `[Unreleased]` does not prove that nothing shipped.
2. Select the next semver without reusing a shipped version. Record the evidence for MAJOR, MINOR,
   or PATCH.
3. Propose the CHANGELOG cut, new empty `[Unreleased]`, compare links, and local version metadata as
   one reviewable diff.
4. Draft—but do not run—the annotated-tag, tag-push, and host Release steps in
   `references/release-commands.md`. A tag is not a host Release.
5. Emit one `releasebench.release-preparation/v1` with selected version, exact local diff, test evidence,
   and the separately closed tag/push/host-Release actions.

## Non-goals and gates

- Do not create even a local tag in this candidate lane.
- Do not push, create or backfill a host Release, contact a host, or query a remote.
- Do not prepare or publish a registry artifact (`releasebench-prepare-package`).
- Do not infer a remote project URL that the owner deferred.

## Feedback loop

Propose reviewable changes to `LESSONS.md`; never silently edit it during a release task.

## Bundled files

- `references/release-commands.md` - gated tag and host Release command shapes.
- `evals/evals.json` - four preserved source eval cases under the canonical ID.
- `scripts/read-lessons.mjs` - internal lesson-reader copy.
