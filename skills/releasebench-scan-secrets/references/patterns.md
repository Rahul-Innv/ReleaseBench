# What scan-secrets.mjs detects (and what it doesn't)

The scanner runs three read-only checks against a git repo's **working tree + tracked files** (via
`git ls-files`). It never writes, deletes, or makes network calls.

## 1. Git-tracked sensitive files
| Severity | Match |
|---|---|
| CRITICAL | a tracked `.env` (any `.env`/`.env.<x>` except `.env.example/.sample/.template/.dist`) |
| CRITICAL | `*.pem` `*.key` `*.p12` `*.pfx` `*.keystore` `*.jks` (private keys/certs) |
| CRITICAL | `id_rsa` / `id_dsa` / `id_ecdsa` / `id_ed25519` (SSH private keys) |
| HIGH | `.npmrc` (often holds `_auth`), `credentials`, `.netrc`, `.pgpass`, `service-account*.json` |

## 2. `.gitignore` coverage
Reports MEDIUM when `.gitignore` doesn't clearly cover `.env`, the `.env.*` family, `*.pem`, or
`*.key` (or when there's no `.gitignore`). Conservative: it may suggest a pattern already covered by
a fancier rule — a harmless suggestion.

## 3. Hardcoded secrets in tracked text files
High-signal patterns (binaries, `node_modules/`, `dist/`, `build/`, lockfiles — `*.lock`,
`package-lock.json`, `pnpm-lock.yaml`, `npm-shrinkwrap.json` — and >1 MB files are skipped):

| Severity | Pattern |
|---|---|
| CRITICAL | `-----BEGIN … PRIVATE KEY-----`, AWS `AKIA…` access-key id, Stripe `sk_live_…` |
| HIGH | GitHub `ghp_…` / `github_pat_…`, Slack `xox[baprs]-…`, Google `AIza…` |
| MEDIUM | a generic `api_key|secret|token|password|client_secret|access_token = "…8+ chars…"` assignment |

The MEDIUM generic rule **skips obvious placeholders** (any `your…`-prefixed value like `your-key`
or `your_api_key_here`, `example`, `changeme`, `${VAR}`, `<...>`, repeated chars, `true/false/null`).
Found values are **redacted** in output (`AKI***LE`).

## Limits (state these to the user)
- **No deep git-history scan.** A secret removed from the tree may still live in history. Use
  `trufflehog` or `gitleaks` for history, and enable the host's **push protection / secret scanning**.
- **Not exhaustive.** It targets common, high-signal formats — not every vendor token or
  high-entropy blob. Absence of findings is reassurance, not a guarantee.
- **Triage required.** The MEDIUM generic rule can flag a non-secret; confirm before acting.

## Adding a new pattern
Edit `scripts/scan-secrets.mjs` (`SENSITIVE` or `PATTERNS`) **and** this file together, then add an
eval case in `evals/evals.json` so the new coverage can't silently regress.
