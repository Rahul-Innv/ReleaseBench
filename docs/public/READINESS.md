# ReleaseBench atomic-family readiness status

Target: `SOURCE_READY_STOP_BEFORE_NEXT_RELEASE_ACTIONS`

This is the current source status. ReleaseBench 0.1.0 already exists on GitLab and PyPI without a
matching Git tag or GitLab Release. The candidate does not self-certify, and this document grants
no provider, lifecycle, marketplace, settings, release, publication, or public-state authority.

| Phase | Current local candidate | Still gated |
|---|---|---|
| 1. Ground | The candidate tree is complete and the canonical GitLab project exists. | Final merged bytes and any settings state must be reverified before a future release. |
| 2. Prepare | The focused offline product-contract suite passes with zero failures, zero errors, and zero skips. | Any later outward preparation remains separately gated. |
| 3. Health | The bundled read-only auditor reports zero missing must-haves. The redacted secret scanner is rerun on every git checkout before a commit decision. | No deep-history or provider-backed scan was performed. |
| 4. Governance/config | GitLab issue templates, merge-request template, and local CI definition are present. The auditor recognizes both GitHub and GitLab project surfaces. No runtime configuration contract exists. | Hosted checks remain evidence for their exact head only. |
| 5. Showcase | The README states architecture, limitations, attribution, and roadmap without a traction or hosted-state claim. | Remote image rendering and reachability remain unverified. |
| 6. Host handoff | The publication leaf solely owns future host-write instructions. | Pushes, settings writes, and other host mutations remain owner-gated. |
| 7. Release | PyPI 0.1.0 exists without a matching Git tag or GitLab Release; current changes remain Unreleased. | Never retro-tag 0.1.0. Select a version strictly greater than 0.1.0, then gate its exact commit before tag or Release creation. |
| 8. Publish/verify | Owner handoff separates future actions from read-only verification of existing public state. | New metadata, settings, asset, release, and publication actions remain owner-gated. |
| 9. Package | The Python package builds offline and passes its metadata check. | A new build, authentication, installation, marketplace action, or publication requires a newer committed version and separate approval. |

## Local verdict

`SOURCE_READY_STOP_BEFORE_NEXT_RELEASE_ACTIONS`

The focused suite passes with zero failures, zero errors, and zero skips. Plugin validation and the
remaining local integrity gates run before any commit or lifecycle decision, and a fresh independent
critic must verify the frozen candidate bytes before acceptance.

The source-readiness result authorizes no merge, tag, Release, settings change, package publication,
skill installation, lifecycle change, or archive action. Existing public state and hosted CI may be
read as evidence, but every mutation remains closed pending a new exact owner gate.
