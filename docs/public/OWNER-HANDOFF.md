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

Owner-only steps remaining are: confirm the canonical host identity and private settings; push the
accepted commit and later tag if desired; create a host Release object for the tag; set description,
topics, and avatar; decide visibility; and verify the resulting public state. Credentials stay in
the owner's authenticated CLI or browser and are never pasted into chat or committed here.

## Prepared commands and UI path

Do not run these until `main` equals the independently accepted candidate and a new exact approval
authorizes the corresponding outward step.

```powershell
git push -u origin main
git tag -a v0.1.0 -m "ReleaseBench 0.1.0 - first launch candidate"
git push origin v0.1.0
```

Create the matching host Release in GitLab at **Deploy > Releases > New release**, selecting the
existing `v0.1.0` tag. Set the description, topics, and avatar at **Settings > General > Naming,
topics, avatar**. Change visibility only through **Settings > General > Visibility, project
features, permissions** after the owner explicitly chooses to make the project public.

After visibility changes, a separate read-only verification must check the host project API,
Releases, latest pipeline, and README asset reachability. That public verification is deliberately
not part of this local packet.
