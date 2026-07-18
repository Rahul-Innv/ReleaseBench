# Changelog

## [Unreleased]

### Added

- Added a `--help`/`-h` fast path to the `releasebench` console entry point documenting the
  request-file interface, exit codes, and the Windows byte-order-mark pitfall.

### Changed

- Rewrote README.md for external readers and moved the detailed do-not-do ledger to STATUS.md.

## [0.1.0] - candidate

### Added

- Added exactly ten canonical atomic skills: one dispatch-only router and nine single-outcome leaves.
- Added deterministic typed routing, positive/near-miss/collision fixtures, and focused offline tests.
- Added private Claude Code plugin packaging under the ReleaseBench identity.
- Added Python packaging for the deterministic router: a `releasebench` module and console entry
  point with identical routing behavior.
- Added MIT governance, contribution, conduct, security, roadmap, validation, readiness, and
  owner-handoff documentation.
- Added a local GitLab CI definition that runs the focused offline product-contract suite.

### Changed

- Internalized the repository preparation, health audit, secret scan, governance scaffold, and
  config-documentation capabilities under ReleaseBench ownership.
- Preserved the exact 49-case eval corpus under per-leaf case IDs.
- Kept every remote, provider, registry, marketplace, installation, publication, public-verification,
  tag, and host action closed.
- Prepared semantic plugin and package metadata without creating a local tag, host Release, or public
  artifact.
