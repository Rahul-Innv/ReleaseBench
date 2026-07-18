# GitHub meta-file templates

Copy each block into the path in its heading, replacing `{{...}}` placeholders.

## `.github/ISSUE_TEMPLATE/bug_report.md`
```markdown
---
name: Bug report
about: Report a problem
title: "[bug] "
labels: bug
---

**What happened?**
A clear description.

**To reproduce**
Steps / the command you ran.

**Expected behavior**
What you expected instead.

**Environment**
- OS:
- {{RUNTIME}} version:

**Logs / output**
Paste relevant output. ⚠️ Do NOT paste secrets or the contents of your `.env`.
```

## `.github/ISSUE_TEMPLATE/feature_request.md`
```markdown
---
name: Feature request
about: Suggest an improvement
title: "[idea] "
labels: enhancement
---

**The problem / motivation**
What's hard today?

**Proposed solution**
What you'd like to see.

**Alternatives considered**
Other approaches.
```

## `.github/ISSUE_TEMPLATE/config.yml`
```yaml
blank_issues_enabled: true
contact_links:
  - name: Security vulnerability (report privately)
    url: https://github.com/{{OWNER}}/{{REPO}}/security/advisories/new
    about: Please report security issues privately, not as a public issue. See SECURITY.md.
```

## `.github/PULL_REQUEST_TEMPLATE.md`
```markdown
## What & why
<!-- What does this change, and why? Link any issue. -->

## How I tested
- [ ] {{TEST_COMMAND}} passes

## Checklist
- [ ] No machine-generated files hand-edited (unless that is the fix)
- [ ] No new dependencies (or an issue agreed one)
- [ ] No secrets staged (`git status` shows no `.env` / keys)
- [ ] Tests added/updated for new behavior
```

## `.gitignore` secrets/keys block (append if missing)
```gitignore
# Secrets — never commit
.env
.env.*
!.env.example
.env.local
.env.backup
*.pem
*.key
```
