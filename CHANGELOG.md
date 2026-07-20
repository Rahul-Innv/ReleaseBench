# Changelog

## [Unreleased]

## [0.1.1] - 2026-07-19

### Added

- Added a `--help`/`-h` fast path to the `releasebench` console entry point documenting the
  request-file interface, exit codes, and the Windows byte-order-mark pitfall.
- Added dependency-free Node regressions for GitHub/GitLab audit parity and documented
  secret-placeholder classification, run in the existing Node CI lane.

### Changed

- Rewrote README.md for external readers and moved the detailed do-not-do ledger to STATUS.md.
- Made repository audits host-aware, kept real secret-like assignments visible while ignoring the
  documented length placeholders, added package project URLs, and collapsed exact receipt examples.
- Kept the Python contract lane Python-only and moved Node-dependent coverage to the Node lane so
  both CI jobs remain self-contained without runtime package installation.
- Kept the scanner regression at integration depth: the Node lane scans this repository and a
  tracked git fixture containing both an ignored documented placeholder and a reported assignment.
- Replaced stale 0.1.0 first-release and retro-tag instructions with a fail-closed next-version
  handoff that requires a committed version strictly greater than the published package.

This patch release has no compare link because the published `0.1.0` package has no matching source
tag. The historical package must not be retro-tagged to manufacture provenance.

## [0.1.0] - 2026-07-18

PyPI records the earliest 0.1.0 distribution upload on 2026-07-18. There is no matching Git tag or
GitLab Release, and this changelog entry does not claim either form of source provenance.

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
- Published the 0.1.0 Python package to PyPI without creating a matching local tag or GitLab
  Release; package publication alone does not establish source provenance.
