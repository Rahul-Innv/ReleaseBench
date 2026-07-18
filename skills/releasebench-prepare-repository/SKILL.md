---
name: releasebench-prepare-repository
description: >-
  Produces one local repository-preparation receipt by coordinating the canonical ReleaseBench audit,
  secret scan, config documentation, and governance-scaffolding leaves, then re-auditing. Use for a
  complete local open-source-readiness or private pre-public preparation pass. For one concern, use
  the matching atomic leaf. Stops on missing decisions and before every host, remote, registry,
  publication, lifecycle, or other outward action.
---

!`node "${CLAUDE_SKILL_DIR}/scripts/read-lessons.mjs" 2>/dev/null || cat "${CLAUDE_SKILL_DIR}/LESSONS.md" 2>/dev/null`

# Preparing for open source

Take a repo from "private and rough" to "public and fork-friendly" in one guided pass. This skill
**coordinates** the focused skills — it doesn't re-implement them.

## When to use this
The user wants one complete local preparation result. For one concern, use the focused leaf directly
(just secrets → `releasebench-scan-secrets`; just files → `releasebench-scaffold-governance`).

## Procedure (run in order; see `references/checklist.md`)
1. **Audit** — run `releasebench-audit-repository` to get the present-vs-missing gap report.
2. **Secrets** — run `releasebench-scan-secrets`; resolve any CRITICAL/HIGH before anything goes public
   (rotate-then-purge for a committed secret).
3. **Config** — if the repo has a JSON config a forker edits, run `releasebench-document-config` for a
   schema + validator + "Make it yours" section.
4. **Scaffold** — run `releasebench-scaffold-governance` to generate ONLY the files the audit flagged missing
   (proposed as reviewable diffs; never overwrite).
5. **Re-audit** — run `releasebench-audit-repository` again; confirm 0 must-haves missing.
6. **Hand off the human-only steps** — from `references/checklist.md`: enable secret scanning + push
   protection + private vulnerability reporting, fill the About panel, ("Use this template" if
   relevant), then make the repo public — these are GitHub-settings clicks the user does; a skill
   cannot.

Stop and surface anything that needs an owner decision (license choice, a personal email in config,
an unresolved secret) rather than guessing.

## Security & altitude
Coordinates other skills; its writes happen only via the sub-skills — `releasebench-scaffold-governance`
(proposed as new files, never overwriting), `releasebench-document-config` (schema + validator + README
section, and in-place config edits: adds `$schema`, removes `_comment` keys), and
`releasebench-scan-secrets`' proposed fixes — all surfaced for owner review. No commits, no host or
registry reads, no tags, no make-public action, and no network of its own.

## Improve this skill (feedback loop)
When the user adjusts the flow (reorder a step, add a check, skip one for private repos), **propose a
reviewable diff** to `LESSONS.md` (schema in that file) — never edit silently. Cross-project
preferences go to Claude's memory.

## Bundled files
- `references/checklist.md` — the full sequence + the human-only GitHub steps.
- `scripts/read-lessons.mjs` — lessons injection.
- `evals/evals.json` — the eval set.
