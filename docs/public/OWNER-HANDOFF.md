# Owner-only outward-action handoff

This packet is preparation, not authorization. Run none of these actions until the local candidate
is independently accepted and the owner supplies a new exact outward approval.

Record the locally configured origin, without contacting it, immediately before any outward step.
This document deliberately names no remote project URL.

Proposed project description:

> ReleaseBench takes private repositories to an evidence-backed pre-publication checkpoint while
> preserving explicit owner gates.

Proposed topics:

`claude-code`, `developer-tools`, `open-source`, `repo-readiness`, `release-automation`

The repository and the 0.1.0 PyPI package already exist publicly. The prepared next source version is
`0.1.1`. Owner-only steps remaining are: merge an independently accepted candidate; create `v0.1.1`
from that exact versioned commit; create the matching GitLab Release; decide any settings changes;
publish the matching package; and verify the resulting public state. Credentials stay in the
owner's authenticated CLI or browser and are never pasted into chat or committed here. Never create
a retroactive `v0.1.0` tag or Release: the published package has no verified source tag provenance.

## Prepared commands and UI path

Do not run these until `main` equals the independently accepted candidate, every version surface and
the changelog name `0.1.1`, the complete release gate passes from that exact commit, and a new exact
approval authorizes the corresponding outward step.

```powershell
$releaseVersion = python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])"
if ($releaseVersion -ne '0.1.1') { throw 'The accepted source is not the prepared 0.1.1 candidate.' }
git tag -a "v$releaseVersion" -m "ReleaseBench $releaseVersion"
git push origin "v$releaseVersion"
```

Create the matching host Release in GitLab at **Deploy > Releases > New release**, selecting the
new `v$releaseVersion` tag. Set the description, topics, and avatar at **Settings > General >
Naming, topics, avatar**. Change any visibility or project feature only through **Settings >
General > Visibility, project features, permissions** after explicit owner approval.

After any outward action, a separate read-only verification must check the host project API,
Release/tag binding, exact-head pipeline, README asset reachability, and PyPI version/project URLs.
That public verification is deliberately not part of this local packet.
