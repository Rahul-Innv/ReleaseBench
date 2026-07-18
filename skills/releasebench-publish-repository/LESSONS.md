# Lessons - releasebench-publish-repository

<!-- counts: captured: 2 | promoted: 0 | superseded: 0 -->

Corrections/preferences for this skill, injected at invocation. **Rules here override SKILL.md on
conflict.** Keep ≤ 100 lines; hold only your own vetted content; **supersede** stale entries. Promote a
`verified`+`high` "rule ignored" entry into SKILL.md with MUST language and retire it here.

Entry schema:
```
- id: L-NNN | date: YYYY-MM-DD | status: proposed|verified|superseded | confidence: low|med|high
  rule: <smallest general rule> | when: <context> | supersedes: <id|none>
```

## Current method
- id: L-001 | date: 2026-07-08 | status: proposed | confidence: high
  rule: Assessment mode on a PRIVATE hosted repo needs AUTHENTICATED read-only host API calls (token
    from env/credential file, never printed); keep authenticated-private checks separate from the
    unauthenticated-public verification you run AFTER it's public.
  when: verifying a repo that is still private
  supersedes: none
- id: L-002 | date: 2026-07-08 | status: proposed | confidence: high
  rule: GitLab path-based project lookup (OWNER%2FNAME) can 404 even with a valid token; fall back to
    the NUMERIC project id (record it once) or a membership search.
  when: a GitLab API path lookup 404s with a valid token
  supersedes: none

<details><summary>Deprecated / superseded</summary>

_(move superseded entries here)_

</details>
