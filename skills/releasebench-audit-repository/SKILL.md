---
name: releasebench-audit-repository
description: >-
  Audits a repository's open-source readiness — checks for the governance and forkability files a
  public repo needs (a LICENSE with a real copyright, README, CONTRIBUTING/SECURITY/CODE_OF_CONDUCT/
  CHANGELOG, .gitignore, issue & PR templates, CI, a package.json license) and reports what's present
  vs missing by severity. Use for a read-only repository launch-readiness, governance, community
  health, or missing-file audit. It reports gaps only and never scaffolds, edits, scans secret values,
  contacts a host, or publishes.
---

!`node "${CLAUDE_SKILL_DIR}/scripts/read-lessons.mjs" 2>/dev/null || cat "${CLAUDE_SKILL_DIR}/LESSONS.md" 2>/dev/null`

# Auditing repo health

Give a fast, honest read on whether a repo is ready to go public — what's there, what's missing, and
what to do next. Read-only: it reports, it doesn't change anything.

## When to use this
The user wants to know if a repo is ready to open-source / go public, to audit repo or community
health, or what governance files are missing. NOT for: reviewing code for bugs, or fixing CI.

## Procedure
1. **Scan (deterministic).** Run the bundled read-only auditor on the repo root:
   `node ${CLAUDE_SKILL_DIR}/scripts/audit-repo.mjs <repo-dir>`. It reports present vs missing files
   by severity (MUST-have: LICENSE with a real copyright, README; RECOMMENDED: CONTRIBUTING, SECURITY,
   CODE_OF_CONDUCT, CHANGELOG, .gitignore, issue/PR templates, CI, package.json license) and exits
   non-zero if a MUST-have is missing.
2. **Summarize** the gaps for the user, highest-severity first; don't pad — name only what's missing.
3. **Route to the fixers** (don't do their jobs here):
   - Missing governance files → `releasebench-scaffold-governance`.
   - Committed-secret risk → `releasebench-scan-secrets`.
   - A JSON config without a schema → `releasebench-document-config`.
4. **Note the human-only steps** for going public: enable secret scanning + push protection +
   private vulnerability reporting, turn on "Use this template", fill the About panel (description,
   topics, Pages URL), then change visibility to public — these are GitHub-settings clicks the user
   does, not something a skill can do.

## Security & altitude
Read-only (the audit is a LOW-altitude bundled script; it never writes or calls the network).
Model-invocable; no broad `allowed-tools`.

## Improve this skill (feedback loop)
When the user corrects the audit (a file to also check, a severity to change, a false "missing"),
**propose a reviewable diff** to `LESSONS.md` (schema in that file) — never edit silently. To change
what's audited, update `scripts/audit-repo.mjs` and add an eval case. Cross-project preferences go to
Claude's memory.

## Bundled files
- `scripts/audit-repo.mjs` — the read-only auditor (run it).
- `scripts/read-lessons.mjs` — lessons injection.
- `evals/evals.json` — the eval set.
