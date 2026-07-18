# Open-source readiness checklist

## The automated pass (this orchestrator runs these in order)
1. **Audit** — `releasebench-audit-repository`: what governance/fork-ability files are present vs missing.
2. **Secrets** — `releasebench-scan-secrets`: tracked secret files, `.gitignore` gaps, hardcoded keys.
3. **Config** — `releasebench-document-config` (only if the repo has a JSON config a forker edits): a
   schema + `$schema` ref, a fail-fast validator, and a "Make it yours" README section.
4. **Scaffold** — `releasebench-scaffold-governance`: generate only files the audit found missing.
5. **Re-audit** — run `releasebench-audit-repository` again to confirm zero must-haves are missing.

## Fork-ability levers (verify, beyond file presence)
- README leads with a **"Make it yours"** path: the few config fields a forker changes + a safe
  offline/dry-run quickstart.
- A **no-financial/▸no-warranty disclaimer** if the tool makes consequential suggestions.
- The watchlist/config has **no personal data** the owner doesn't want public (e.g. a personal email
  that could move to a CI secret instead).

## Closed outward steps

These steps are handoff information only. This candidate cannot execute or verify them without a new
exact owner approval:
- Enable **secret scanning + push protection** (Settings → Code security).
- Enable **Private vulnerability reporting** (same Settings → Code security page) — the scaffolded
  SECURITY.md ("Report a vulnerability" button) and issue config.yml (`/security/advisories/new`
  link) depend on it; without it the button doesn't exist and the link 404s.
- Turn on **"Use this template"** (Settings → General) if it's meant to be forked as a template.
- Fill the **About** panel: description, topics, and the Pages URL if there's a dashboard.
- Rotate any key that was ever committed/exposed **before** going public.
- Change visibility to **Public** (Settings → General → Danger Zone) — last, after the above.
