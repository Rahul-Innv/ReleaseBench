# Offline validation and qualification

This contract defines the evidence required for the ReleaseBench 0.1.0 atomic-family candidate. It
authorizes no outward action and is not an independent acceptance receipt.

## Untouched-base comparison

Record the exact base commit and tree, clean/dirty state, configured remotes without contacting
them, and tags without creating any. Replay the base's applicable local checks separately so a known
baseline failure is never presented as a candidate regression.

## Candidate gates

Run from the isolated candidate root:

```powershell
python -B tests/releasebench/run_tests.py
claude.cmd plugin validate .
git diff --check HEAD
git fsck --strict --no-reflogs
```

The focused suite must report zero failures, zero errors, and zero skips. `.gitlab-ci.yml` runs the
same suite and invokes `node --check` once for every bundled `.mjs` file. The job-script payload
contains no explicit network, provider, registry, marketplace, publication, remote-write, or
credential command. The runner may nevertheless resolve the declared external floating container
images, so hosted execution is not offline-deterministic evidence and remains unverified until a
separate outward gate permits it.

Also:

1. parse every JSON file as UTF-8;
2. run `node --check` on every `.mjs` file;
3. verify all ten `SKILL.md` frontmatter names equal their folder names;
4. verify all ten `agents/openai.yaml` files use canonical default prompts and keep implicit
   invocation disabled;
5. verify the exact 49 eval cases, per-leaf IDs, boolean trigger labels, positives, and near misses;
6. replay all positive routes, near misses, 36 pairwise intent collisions, full-flow progression,
   malformed requests, and CLI/in-process byte parity;
7. build the Python package offline (`python -m build --no-isolation`) and check its metadata
   (`python -m twine check dist/*`);
8. scan for secret values, owner-home paths, and undeclared absolute paths, and verify the router
   has no network or process-execution surface;
9. prove all eight outward modes remain closed; and
10. stage only the exact owned candidate paths, freeze the tree/checksum manifest, and replay it
    from a fresh worktree.

## Privacy and outward boundary

Privacy checks report only file path and finding class, never matched credential values. Generic
instructional placeholders are not owner-path findings.

Qualification performs no fetch, pull, push, remote creation or mutation, tag, host Release,
host/API call, public verification, registry read, authentication, provider call, marketplace
action, package publication, skill installation or promotion, archive mutation, or destructive
cleanup.

## Independent critic

The producing lane sets `self_certification: false`. After the exact staged tree is frozen, a fresh
critic must independently replay the owned-path diff, focused checks, baseline comparison,
closed-action proof, and checksums. The producing lane stops before commit.
