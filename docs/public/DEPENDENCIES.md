# ReleaseBench dependency contract

ReleaseBench owns and bundles exactly ten canonical skills: one dispatch-only router and nine atomic
leaves. The five repository-preparation capabilities that were previously separate are members of
this family:

- `releasebench-prepare-repository`
- `releasebench-audit-repository`
- `releasebench-scan-secrets`
- `releasebench-scaffold-governance`
- `releasebench-document-config`

The remaining members are `releasebench-route`, `releasebench-showcase-readme`,
`releasebench-publish-repository`, `releasebench-release-version`, and
`releasebench-prepare-package`.

## Lifecycle authority

The host environment remains the lifecycle, eligibility, supersession, and routing-priority
authority. Bundling a skill in this repository does not install, activate, promote, or expose it. A
missing member, stale receipt, or unresolved lifecycle collision fails closed.

## Runtime dependencies

The router and the focused test suite require only the Python 3.10+ standard library. The bundled
audit and secret-scan helpers require only a Node.js runtime; they are dependency-free and never
contact the network.

## Closed dependencies

No provider, registry, marketplace, remote host, authentication, or public network dependency is
required or permitted for offline qualification. A leaf that would require one of those surfaces
stops with an evidence-backed handoff instead of substituting an inline implementation or claiming
the external state is verified.
