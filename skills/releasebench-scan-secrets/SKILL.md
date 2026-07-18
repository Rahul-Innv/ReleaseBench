---
name: releasebench-scan-secrets
description: >-
  Audits a repository for leaked-secret risks — git-tracked .env/key files, .gitignore coverage gaps,
  and hardcoded secrets in tracked files — and reports findings by severity with safe fixes. Use when
  the user wants a read-only, redacted secret-hygiene scan before review or publication, to verify
  .gitignore coverage, or to check for committed credentials. It never rotates credentials, rewrites
  history, prints secret values, contacts a provider, or publishes findings.
---

!`node "${CLAUDE_SKILL_DIR}/scripts/read-lessons.mjs" 2>/dev/null || cat "${CLAUDE_SKILL_DIR}/LESSONS.md" 2>/dev/null`

# Checking secrets hygiene

Find secret-leak risks in a repo before they reach a public remote (or in review/CI). Trust is the
point: report honestly, keep findings redacted, and never make a leak worse.

## When to use this
The user wants to check/scan for committed secrets or leaked keys, audit a repo before going public,
confirm `.gitignore` covers secrets, or asks "am I leaking any credentials?". NOT for: writing app
auth/login code, or rotating keys on their behalf (you guide; they rotate).

## Procedure
1. **Scan (deterministic).** Run the bundled read-only scanner on the repo root:
   `node ${CLAUDE_SKILL_DIR}/scripts/scan-secrets.mjs <repo-dir>`. It checks three things — tracked
   sensitive files (.env/keys), `.gitignore` coverage, and hardcoded secrets in tracked text files —
   and prints findings by severity (CRITICAL/HIGH/MEDIUM), redacted. It only reports (no writes) and
   exits non-zero on CRITICAL/HIGH, so it also works in CI. See `references/patterns.md` for exactly
   what it detects and its limits.
2. **Triage.** For each CRITICAL/HIGH, confirm it's a real secret, not a placeholder/example (an
   `.env.example` with empty or `your-key-here` values is fine). Drop confirmed false-positives.
3. **Propose fixes as reviewable diffs — least-harm first:**
   - Missing `.gitignore` patterns → propose the additions.
   - A secret committed to the working tree → fix order is **ROTATE the secret first** (assume it's
     already compromised), then remove it from the tree, then **purge it from git history**
     (`git filter-repo` or BFG) — give the owner the exact command to run; never run the history
     rewrite yourself without explicit confirmation (it is irreversible). Deleting it in a new
     commit is NOT enough — it stays in history.
   - Never echo the full secret back; keep it redacted.
4. **State the limit.** This scans the working tree + tracked files, not deep git history — recommend
   `trufflehog`/`gitleaks` for a history sweep and enabling the host's push-protection/secret-scanning.

## Security & altitude
Read-only by design (the scan is a LOW-altitude bundled script; fixes are MEDIUM, proposed as diffs
the owner applies). The scanner makes no network calls and writes nothing. Model-invocable (scanning
is safe); no broad `allowed-tools`.

## Improve this skill (feedback loop)
When the user corrects a finding (a false positive to suppress, a secret type to add), **propose a
reviewable diff** to `LESSONS.md` (schema in that file) — never edit silently. To add a new secret
pattern, update `scripts/scan-secrets.mjs` + `references/patterns.md` together and add an eval case so
it can't regress. Cross-project preferences go to Claude's memory.

## Bundled files
- `scripts/scan-secrets.mjs` — the read-only scanner (run it).
- `scripts/read-lessons.mjs` — lessons injection.
- `references/patterns.md` — detected secret types, coverage, and limits.
- `evals/evals.json` — the eval set.
