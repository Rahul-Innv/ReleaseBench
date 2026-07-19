# Status

The README carries the product story; this page carries the fine print: where the project stands,
what it deliberately does not do, and the process language its formal documents use.

## Where things stand

- Version `0.1.0` everywhere it is declared: the plugin manifest (`.claude-plugin/plugin.json`),
  the Python package (`pyproject.toml`), and the changelog.
- Published so far: this repository on GitLab and the `releasebench` package on PyPI.
- Distribution: the repository now ships a self-hosted plugin marketplace manifest
  (`.claude-plugin/marketplace.json`) you add by URL in Claude Code. It is not published to any
  external or central marketplace registry, and no skill is listed in a third-party skill directory.
- Not yet done: no git tag and no GitLab Release object.
- The deterministic suite passes: 22 Python contracts (`tests=22 failures=0 errors=0 skipped=0`)
  plus 2 Node tool regressions.

## What ReleaseBench never does on its own

Every skill stops before any action that leaves your machine. Concretely, no ReleaseBench skill
will:

- create a remote project or push to one (including the very first push);
- fetch, pull, create a tag, or create a host Release;
- change repository visibility, description, topics, or avatar;
- call a host or provider API, check whether a remote image is reachable, or perform any other
  network verification;
- query a package registry (even to check name availability), authenticate anywhere, or publish a
  package;
- install, activate, or promote a skill, or perform any marketplace action.

`releasebench-publish-repository` is the only skill concerned with host setup and the first push,
and even it only writes the instructions for the owner to run. In router receipts this list appears
as `closed_actions`, and every receipt records `outward_actions_authorized: false` and
`outward_actions_executed: false`.

## The careful wording, translated

ReleaseBench's formal documents use guarded process language. What it means:

- **"Inactive candidate."** Bundling a skill in a repository does not install, activate, or
  prioritize it anywhere; the host environment (for example, your Claude Code installation) remains
  the authority over skill lifecycle, eligibility, supersession, and routing priority. ReleaseBench
  therefore describes itself as an inactive candidate: present and testable, granting itself no
  authority. Installing the PyPI package likewise changes no skill lifecycle state.
- **"The producing lane does not self-certify."** Whoever (or whatever agent) produces a change
  never approves it. A fresh, independent reviewer must verify the exact frozen bytes before any
  commit or release decision.
- **Codex metadata is present but implicit invocation is off.** Skills run only when named
  explicitly.

## Full local qualification

Beyond the focused suite, a full qualification pass runs:

```powershell
python -B tests/releasebench/run_tests.py
node --test tests/releasebench/test_node_tools.mjs
claude.cmd plugin validate .
git diff --check HEAD
git fsck --strict --no-reflogs
```

then parses every JSON document, runs `node --check` on every bundled `.mjs` script, and replays the
exact staged tree from a fresh worktree.

One caveat about CI: the GitLab CI jobs run only the offline Python suite plus Node syntax and
functional tool regressions, and their scripts contain no network, registry, or publish command,
but the hosted runner still pulls
the declared floating container images (`python:3.12-alpine`, `node:22-bookworm`). Hosted pipeline
results are therefore not claimed as offline-deterministic evidence; the suite run on your own
checkout is the ground truth.

## Internal machinery

Alongside the ten skills, the repository carries three internal, non-skill pieces: a shared lesson
reader script bundled with each skill, the plugin manifest, and a portable agent guide
([AGENTS.md](AGENTS.md), duplicated byte-for-byte inside the router skill). None of these is an
installable skill.

## Naming and source policy

New paths, receipts, invocations, and documentation use canonical ReleaseBench IDs only. This
repository does not modify installed skills, imported packages, remotes, marketplaces, providers, or
archives.

## The formal contracts

- [Readiness ledger](docs/public/READINESS.md): phase-by-phase local status and what remains gated.
- [Validation contract](docs/public/VALIDATION.md): the evidence required before acceptance.
- [Dependency contract](docs/public/DEPENDENCIES.md): what the family owns and bundles.
- [Release candidate](docs/public/RELEASE-CANDIDATE.md): the `0.1.0` version decision.
- [Owner handoff](docs/public/OWNER-HANDOFF.md): the prepared owner-only outward steps.
- [Configuration](docs/public/CONFIGURATION.md): why there is no runtime configuration contract.
