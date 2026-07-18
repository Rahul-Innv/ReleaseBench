# Host metadata + verification commands

Replace `OWNER/NAME`; GitLab API path is URL-encoded as `OWNER%2FNAME`. Token commands are the OWNER's
to run — give them the command with a `<TOKEN>` placeholder; never accept a pasted token in chat. Every
token command has a no-token UI fallback.

## Make public + description + topics (OWNER, token) — GitLab
One PUT sets all three; single line so it pastes into PowerShell or bash:
```bash
curl --request PUT "https://gitlab.com/api/v4/projects/OWNER%2FNAME" --header "PRIVATE-TOKEN: <TOKEN>" --data-urlencode "visibility=public" --data-urlencode "description=<ONE LINE, plain ASCII>" --data "topics[]=claude-code" --data "topics[]=cli" --data "topics[]=automation"
```
No-token UI: **Settings → General → "Naming, topics, avatar"** (description + topics) and
**"Visibility, project features, permissions"** (Public) → Save.

GitHub (owner; `gh` is pre-authed, no raw token):
```bash
gh repo edit OWNER/NAME --visibility public --description "<one line>" --add-topic claude-code,cli,automation
```

## Avatar (OWNER, UI)
GitLab: **Settings → General → "Naming, topics, avatar"** → upload the logo. Some hosts reject SVG
avatars — if refused, upload a PNG export; the README logo works regardless.

## Verify after going public (Claude runs these — unauth, read-only)
The GitLab API returns data only when the project is public, so these double as the visibility check
(replace `main` in the raw-asset URL with the repo's actual default branch):
```bash
P="https://gitlab.com/api/v4/projects/OWNER%2FNAME"
curl -s "$P"                      | grep -oE '"visibility":"[a-z]+"'
curl -s "$P"                      | grep -oE '"topics":\[[^]]*\]'
curl -s "$P/releases"             | grep -oE '"tag_name":"[^"]+"'
curl -s "$P/pipelines?per_page=1" | grep -oE '"status":"[a-z]+"'
curl -s -o /dev/null -w "%{http_code}\n" "https://gitlab.com/OWNER/NAME/-/raw/main/demo.svg"
```
GitHub: `gh repo view OWNER/NAME --json visibility,repositoryTopics`, `gh release list`,
`gh run list --limit 1`, and a `curl` on the `raw.githubusercontent.com` path.

Report each result explicitly; if the API returns nothing, the repo is still private (or unreachable).
