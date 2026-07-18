# Security Policy

## Reporting a vulnerability

**Please do not open a public issue for security problems.**

Report privately via GitHub's **Private vulnerability reporting**: the repo's **Security** tab →
**Report a vulnerability**. If that isn't available, open a minimal public issue saying *only* that
you'd like a private security contact (no details), and the maintainer will set up a channel.

Include: what the issue is and where, how to reproduce it, and the potential impact.

This is a {{PROJECT_SCALE}} project, so responses are best-effort — but security reports are taken
seriously and prioritized over features.

## Supported versions
Only the current `{{DEFAULT_BRANCH}}` branch is supported.

## Secrets & security posture
- Secrets live only in environment variables / CI secrets — **never committed**. `.env` and key files
  (`*.pem`, `*.key`, `.env.local`, `.env.backup`) are gitignored.
- If a key is ever exposed, **rotate it immediately** — treat anything that touched a commit, log, or
  transcript as compromised.
- {{NO_SECRETS_IN_CLIENT_NOTE}}
- Output from third-party/untrusted sources is escaped/sanitized before rendering.
