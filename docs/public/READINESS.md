# ReleaseBench atomic-family readiness status

Historical target: `SOURCE_READY_STOP_BEFORE_NEXT_RELEASE_ACTIONS`

Current release state, verified 2026-09-25: the `v0.1.1` tag and GitLab Release
exist, and PyPI publishes `releasebench` `0.1.1`. The table below records the
pre-release candidate review. It is retained as history, not as a current
publication checklist or evidence of skill activation.

| Phase | Current local candidate | Still gated |
|---|---|---|
| 1. Ground | The candidate tree is complete and the canonical GitLab project exists. | Final merged bytes and any settings state must be reverified before a future release. |
| 2. Prepare | The focused offline product-contract suite passes with zero failures, zero errors, and zero skips. | Any later outward preparation remains separately gated. |
| 3. Health | The bundled read-only auditor reports zero missing must-haves. The redacted secret scanner is rerun on every git checkout before a commit decision. | No deep-history or provider-backed scan was performed. |
| 4. Governance/config | GitLab issue templates, merge-request template, and local CI definition are present. The auditor recognizes both GitHub and GitLab project surfaces. No runtime configuration contract exists. | Hosted checks remain evidence for their exact head only. |
| 5. Showcase | The README states architecture, limitations, attribution, and roadmap without a traction or hosted-state claim. | Remote image rendering and reachability remain unverified. |
| 6. Host handoff | The publication leaf solely owns future host-write instructions. | Pushes, settings writes, and other host mutations remain owner-gated. |
| 7. Release | PATCH version 0.1.1 is selected and the dated changelog cut is prepared; PyPI 0.1.0 remains provenance-unknown. | Never retro-tag 0.1.0. Independently accept the exact 0.1.1 commit before any `v0.1.1` tag, GitLab Release, or package publication. |
| 8. Publish/verify | Owner handoff separates future actions from read-only verification of existing public state. | New metadata, settings, asset, release, and publication actions remain owner-gated. |
| 9. Package | The 0.1.1 Python package candidate builds offline and passes its metadata check. | Authentication, installation, marketplace action, or publication requires separate approval. |

## Local verdict

`SOURCE_READY_STOP_BEFORE_NEXT_RELEASE_ACTIONS`

The focused suite passes with zero failures, zero errors, and zero skips. Plugin validation and the
remaining local integrity gates run before any commit or lifecycle decision, and a fresh independent
critic must verify the frozen candidate bytes before acceptance.

The source-readiness result authorizes no merge, tag, Release, settings change, package publication,
skill installation, lifecycle change, or archive action. Existing public state and hosted CI may be
read as evidence, but every mutation remains closed pending a new exact owner gate.
