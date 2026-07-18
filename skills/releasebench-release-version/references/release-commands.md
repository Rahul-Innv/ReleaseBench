# Release commands

Replace `OWNER/NAME`; GitLab API path is URL-encoded as `OWNER%2FNAME`. Token commands are the OWNER's
to run — give them the command with a `<TOKEN>` placeholder; never accept a pasted token in chat.

## CHANGELOG cut (Keep a Changelog)
Move `[Unreleased]` under `## [x.y.z] — YYYY-MM-DD`, add a fresh empty `[Unreleased]`, and update the
compare links, e.g.:
```
[Unreleased]: https://gitlab.com/OWNER/NAME/-/compare/vX.Y.Z...main
[X.Y.Z]: https://gitlab.com/OWNER/NAME/-/compare/vPREV...vX.Y.Z
```

## Git tag (after confirmation)
```bash
git tag -a vX.Y.Z -m "NAME X.Y.Z — <one-line>"
git push origin vX.Y.Z        # outward — confirm first
```

## Host Release object — one per tag (a tag is NOT a Release)
GitLab (owner token):
```bash
curl --request POST "https://gitlab.com/api/v4/projects/OWNER%2FNAME/releases" --header "PRIVATE-TOKEN: <TOKEN>" --data-urlencode "name=NAME X.Y.Z" --data-urlencode "tag_name=vX.Y.Z" --data-urlencode "released_at=YYYY-MM-DDT00:00:00Z" --data-urlencode "description=<notes; markdown ok>"
```
GitLab no-token UI: **Deploy → Releases → New release** → pick the existing tag → title + notes → Create.
Backdate `released_at` to the CHANGELOG date when backfilling older tags.

GitHub:
```bash
gh release create vX.Y.Z --title "NAME X.Y.Z" --notes "<notes>"
```

## Backfill check
List tags (`git tag -l`) and existing Releases; create a Release for every tag that lacks one so the
Releases page shows the full history.
