# Lessons - releasebench-showcase-readme

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
  rule: For a freshly-published repo with no usage/download/deployment traction yet, do NOT fabricate a
    "proven in the real world" section. A documented honest-validation/limitations section (tested vs
    not, earned vs unearned modes) IS the integrity proof — link real artifacts (test count, runnable
    demo OUTPUT, a benchmark harness) instead of invented metrics.
  when: showpiece proof section on a repo with no real traction yet
  supersedes: none
- id: L-002 | date: 2026-07-08 | status: verified | confidence: high
  rule: Check README/CHANGELOG/readiness prose against the repo's CURRENT verified state — stale "next
    steps" / "known gaps" mislead as much as missing proof; treat cross-doc inconsistency as a release
    blocker.
  when: showpiece pass on a repo whose CI/proof/metadata was recently completed
  supersedes: none

<details><summary>Deprecated / superseded</summary>

_(move superseded entries here)_

</details>
