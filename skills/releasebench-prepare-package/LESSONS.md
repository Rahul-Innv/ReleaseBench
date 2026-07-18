# Lessons - releasebench-prepare-package

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
  rule: Derive the `files` whitelist from the repo's ACTUAL runtime layout (read main/bin + source
    dirs), not the `bin/lib/scripts` example — a repo may keep runtime in sensor/ trigger/ bin/ skills/
    with no lib/. And FIRST assess whether npm is even the right channel: a settings.json-hook-wired
    tool isn't npm-distributed just because it has a package.json + bin.
  when: readying a non-standard-layout or non-library repo for npm
  supersedes: none
- id: L-002 | date: 2026-07-08 | status: proposed | confidence: high
  rule: Registry availability is NOT readiness — a free name doesn't mean the package is publishable.
    Verify a real publishable layout: build-system/manifest, entry point, and a successful build +
    dry-run (npm pack / python -m build + twine check / cargo publish --dry-run), not just the name.
  when: package-registry phase sees a manifest but no proven build
  supersedes: none

<details><summary>Deprecated / superseded</summary>

_(move superseded entries here)_

</details>
