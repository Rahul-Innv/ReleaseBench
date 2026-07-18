---
name: releasebench-prepare-package
description: >-
  Prepares a distributable package with manifest metadata, an exact runtime-files allowlist,
  entrypoint checks, and an offline build or package dry run. Use for npm, PyPI, cargo, gem, or other
  package-readiness and "what would ship?" requests. First proves that a registry channel actually
  applies. In this private candidate it never queries package-name availability, authenticates,
  contacts a registry, claims a name, or publishes.
---

!`node "${CLAUDE_SKILL_DIR}/scripts/read-lessons.mjs" 2>/dev/null || cat "${CLAUDE_SKILL_DIR}/LESSONS.md" 2>/dev/null`

# Prepare a package offline

Produce one evidence-bound package dry-run receipt. Publication is not part of this outcome.

## Procedure

1. Confirm the repository is genuinely registry-distributed. A manifest or CLI alone is not proof.
2. Read the actual runtime layout and entrypoints. Prepare publishable metadata and a files allowlist
   that includes runtime + required docs/assets and excludes tests, CI, evidence, secrets, and junk.
3. Check ecosystem entrypoint requirements, such as a Node CLI shebang, without installing or
   contacting anything.
4. Run only the ecosystem's offline build or dry-run command when its dependencies are already
   available locally. Inspect the exact artifact/file list and record its hash and size.
5. Emit one `releasebench.package-preparation/v1` with channel applicability, manifest diff, artifact
   inventory, validation output, and the closed registry-query/authentication/publication actions.

Registry-specific offline shapes are in `references/other-registries.md`. Network availability checks
and publish commands remain owner-gated reference material only.

## Non-goals and gates

- Do not run `npm view`, `pip index`, `cargo search`, or any registry/network availability check.
- Do not authenticate, claim a name, upload, publish, or change remote state.
- Do not cut a repository version (`releasebench-release-version`) or publish a host repository
  (`releasebench-publish-repository`).
- Do not install missing build dependencies without a separate gate.

## Feedback loop

Propose reviewable changes to `LESSONS.md`; never silently edit it during package preparation.

## Bundled files

- `references/other-registries.md` - ecosystem mapping with current outward gates applied.
- `evals/evals.json` - four preserved source eval cases under the canonical ID.
- `scripts/read-lessons.mjs` - internal lesson-reader copy.
