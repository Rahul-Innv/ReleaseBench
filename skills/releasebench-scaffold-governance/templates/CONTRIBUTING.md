# Contributing to {{PROJECT_NAME}}

Thanks for your interest! Please read the guardrails below before opening a PR.

## Ground rules (fill in this project's specifics)
<!-- Replace with the project's real, non-negotiable rules. Examples to adapt:
- How to run safely without spending money / sending anything / hitting live services.
- Files that are machine-generated and must NOT be hand-edited.
- Dependency policy (e.g. "no new runtime dependencies without an issue first").
- Accuracy / correctness invariants specific to this project. -->
- {{GUARDRAIL_1}}
- {{GUARDRAIL_2}}
- {{GUARDRAIL_3}}

## Dev setup
- Install: `{{INSTALL_COMMAND}}`
- Run the tests: `{{TEST_COMMAND}}`
- {{OFFLINE_OR_DRY_RUN_NOTE}}

## Making a change
1. Fork and create a branch (`git checkout -b my-change`).
2. Make a focused change that matches the surrounding style.
3. **Add or update tests** and make sure `{{TEST_COMMAND}}` passes.
4. Open a pull request describing **what** changed and **why**, and note any guardrail it touches.

### Commit checklist
- [ ] Tests pass (`{{TEST_COMMAND}}`).
- [ ] No machine-generated files hand-edited (unless that *is* the fix, explained).
- [ ] No new dependencies (or an issue agreed one).
- [ ] No secrets staged — `git status` shows no `.env` / keys / `*.pem` / `*.key`.

## Reporting bugs & security issues
Open an [issue](../../issues) for bugs and ideas. For anything security-sensitive, follow
[SECURITY.md](SECURITY.md) instead of a public issue.
