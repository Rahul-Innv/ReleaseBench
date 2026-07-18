# Contributing to ReleaseBench

Thank you for helping improve ReleaseBench. Contributions should strengthen the repository-launch
workflow without weakening its owner-approval, privacy, or evidence requirements.

## Before proposing a change

1. Read `AGENTS.md` and the affected skill's `SKILL.md`, `LESSONS.md`, and backlog.
2. Keep the router and leaf skills consistent across Claude Code and portable agent surfaces.
3. Do not include credentials, private repositories, owner home paths, browser state, or private
   customer/project data in fixtures, examples, screenshots, or logs.
4. Add or update an evaluation when behavior, routing, safety gates, or output contracts change.

## Validation

Run the focused product-contract suite, the available plugin validator, and the affected skill
evaluations. Record the exact commands and results in the merge request. If a validator is
unavailable, say so rather than representing the change as fully verified.

```powershell
python -B tests/releasebench/run_tests.py
claude.cmd plugin validate .
```

The focused suite must pass with zero failures, zero errors, and zero skips before a release
candidate is accepted.

Keep commits focused and explain any intentional compatibility break. Do not publish, tag, or change
project visibility as part of a contribution unless the owner separately approves that outward
action.

## Merge requests

Describe:

- the problem and intended behavior;
- the skills and surfaces affected;
- tests/evaluations run and their results;
- privacy, compatibility, or migration considerations;
- any owner-only action that remains.
