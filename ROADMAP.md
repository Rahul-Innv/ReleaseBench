# ReleaseBench roadmap

ReleaseBench is pre-1.0. This sequence is not a promise of dates or lifecycle eligibility.

## Atomic private candidate

- [x] Define exactly ten canonical skills with one measurable outcome each.
- [x] Keep the router dispatch-only and fail closed on ambiguity.
- [x] Preserve the 49-case eval corpus, templates, assets, lesson readers, references, scripts, and
  portable guidance.
- [x] Add canonical Claude Code and inactive Codex metadata.

## Private launch readiness

- [x] Run the focused offline product-contract suite with zero failures, zero errors, and zero skips.
- [x] Add a local GitLab CI definition for the offline suite.
- [x] Package the deterministic router as an installable Python module with a console entry point.
- [x] Record the published 0.1.0 package without inventing a matching Git tag or GitLab Release.
- [ ] Select and commit a version strictly greater than 0.1.0 before any future release candidate.
- [ ] Replay the final staged tree from a fresh isolated worktree.
- [ ] Verify no new regression against the untouched base.
- [ ] Run provider-backed trigger evaluation only after separate provider approval.
- [ ] Resolve any product decisions identified by independent qualification.
- [ ] Merge only by a separately approved clean fast-forward path.

## Public-launch gate

- [ ] Recheck privacy, security, licenses, dependencies, and disclosure choices.
- [ ] Verify README claims from the exact release candidate.
- [ ] Confirm the canonical host project URL and private host state separately.
- [ ] Decide and approve tag, host Release, metadata, avatar, visibility, and public verification.
- [ ] Install or promote skills only through a separate owner lifecycle decision.
- [ ] Publish no new package or marketplace artifact without a newer committed version and a new
  exact owner approval.
