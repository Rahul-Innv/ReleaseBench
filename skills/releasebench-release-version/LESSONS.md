# Lessons - releasebench-release-version

<!-- counts: captured: 1 | promoted: 0 | superseded: 0 -->

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
  rule: Before cutting, diff commits since the last tag against CHANGELOG [Unreleased]; an EMPTY
    [Unreleased] does NOT mean nothing shipped — warn on shipped-but-unlogged work.
  when: release cut where commits exist since the last tag
  supersedes: none

<details><summary>Deprecated / superseded</summary>

_(move superseded entries here)_

</details>
