---
name: releasebench-scaffold-governance
description: >-
  Generates only the missing open-source governance files for a repo — LICENSE (MIT), CONTRIBUTING,
  SECURITY, CODE_OF_CONDUCT, CHANGELOG, GitHub issue & PR templates, and a .gitignore secrets block —
  from templates filled with the project's specifics, proposed as reviewable diffs that never
  overwrite existing files. Use to add missing LICENSE, CONTRIBUTING, SECURITY, conduct, changelog,
  issue, or merge-request templates. It does not document config, polish README content, publish,
  commit, or guess unresolved owner details.
---

!`node "${CLAUDE_SKILL_DIR}/scripts/read-lessons.mjs" 2>/dev/null || cat "${CLAUDE_SKILL_DIR}/LESSONS.md" 2>/dev/null`

# Scaffolding OSS files

Create the governance files a public, fork-friendly repo needs — filled with the project's real
details, not generic boilerplate, and proposed for review.

## When to use this
The user wants to add/scaffold/create LICENSE, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CHANGELOG, or
GitHub issue/PR templates, or set up the files to make a repo public. NOT for: a JSON config schema
(use `releasebench-document-config`) or app/README content.

## Procedure
1. **Only scaffold what's missing.** First run `releasebench-audit-repository` (or its `audit-repo.mjs`) and
   scaffold ONLY the files it reports missing.
2. **Gather the specifics** — project name, owner/handle, year, license choice, test command, default
   branch, security contact. Infer what you can from the repo (`package.json`, the git remote); ask
   the user for the rest. Don't leave `{{PLACEHOLDERS}}` in the output.
3. **Fill the templates.** Read the matching file from `templates/` (`LICENSE-MIT.txt`,
   `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`, and `github-meta.md` for
   the issue/PR/`.gitignore` blocks), replace every placeholder, and **propose each as a NEW file**.
4. **Never overwrite.** If a target file already exists, do NOT clobber it — show a diff of your
   proposed version and let the owner decide. This skill creates files (a side effect), so it works by
   proposing reviewable changes, never silent writes.
5. **Harden `.gitignore` additively** — append the secrets block from `github-meta.md` only if those
   patterns are missing; never reorder or remove existing lines.
6. **Summarize** what was created and the remaining human-only steps (fill the About panel, enable
   secret scanning + push protection + private vulnerability reporting — SECURITY.md and the issue
   config link to it — then make the repo public).

## Security & altitude
Generative (MEDIUM altitude — templates the project customizes). It creates local files only — no
commits, no network, no overwrites without review. Model-invocable BY DESIGN —
`disable-model-invocation` would also block `releasebench-prepare-repository`'s Skill-tool call (step 4 of
its pass); the propose-only/never-overwrite posture is the gate instead. No broad `allowed-tools`.

## Improve this skill (feedback loop)
When the user states a preference (a default license, a house CONTRIBUTING style, a CoC contact),
**propose a reviewable diff** to `LESSONS.md` (schema in that file) — never edit silently. To change a
template, edit it under `templates/`. Cross-project preferences go to Claude's memory.

## Bundled files
- `templates/` — `LICENSE-MIT.txt`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
  `CHANGELOG.md`, `github-meta.md` (issue/PR/.gitignore blocks).
- `scripts/read-lessons.mjs` — lessons injection.
- `evals/evals.json` — the eval set.
