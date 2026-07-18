---
name: releasebench-showcase-readme
description: >-
  Runs a README showpiece pass on a repo: adds CI/license/runtime badges, a "proven in the real world"
  proof section, a demo, a mermaid architecture diagram, real-name attribution, and a ROADMAP; and
  generates a self-contained demo.svg and logo.svg when a real screen recording isn't possible. Use when
  the user wants to make a README look premium/portfolio-grade, add badges or an architecture diagram,
  add a demo or logo, write a proof/traction section, or polish the repo's storefront for a public/YC
  audience. Keeps everything true, uses real generic command output, and excludes owner-private data.
  Use only for the README storefront and its local assets. Not for governance scaffolding
  (`releasebench-scaffold-governance`) or host publication (`releasebench-publish-repository`).
---

!`node "${CLAUDE_SKILL_DIR}/scripts/read-lessons.mjs" 2>/dev/null || cat "${CLAUDE_SKILL_DIR}/LESSONS.md" 2>/dev/null`

# Showcasing a repo README

Make the README read as a premium, portfolio-grade storefront. A reviewer decides in ~20 seconds — order
the top so it reads: logo → title → badges → one-line pitch → proof → demo → what-it-is → architecture
diagram → quick start. Add only what is TRUE.

## MUST
- Everything shown is true: no invented metrics, fake stars, or fabricated demos.
- A demo must use the tool's REAL command/output strings (capture `<cmd> --help` / a real status line
  first) and a GENERIC example — NEVER the owner's private data.
- Local edits only here; don't push (the router / publish step handles that). Flag when a change is
  ready to commit.

## Steps
1. **Badges** under the title — CI pipeline, license, language/runtime. Snippets: `references/readme-snippets.md`.
2. **Proof** — a "Proven in the real world" section stating a real, verifiable outcome (scale/cost/when),
   private data stripped. The single most persuasive block for a portfolio/YC piece.
3. **Demo** — prefer a real screen recording. When impossible, generate a self-contained `demo.svg`
   (copy `assets/demo.svg`, adapt every line to this tool's real output) and embed it with a
   repo-relative path.
4. **Architecture diagram** — a ```mermaid block capturing the core insight (not every file); renders on
   GitLab and GitHub.
5. **Logo** — copy `assets/logo.svg`, recolor to the palette; add a centered header `<img>` and hand it
   to the publish step for the project avatar.
6. **Attribution + roadmap** — real name in `LICENSE` + a "Built by <Name>." line; add `ROADMAP.md`
   stating the deliberate current scope, then near-term / later / non-goals.
7. Note what you added in the CHANGELOG `[Unreleased]`. Verify every referenced image resolves.

## Anti-patterns
- Invented metrics / a fabricated demo / the owner's private data as the example.
- Leaving a "recording coming" placeholder on a public README — ship the SVG or remove the placeholder.

## Improve this skill (feedback loop)
When the user corrects your output or states a reusable preference, **propose a reviewable diff**
appending one entry to `LESSONS.md` — never edit silently. Promote a verified, high-confidence "rule
was ignored" lesson into this body with MUST language. Cross-project preferences go to Claude Code memory.

## Bundled files
- `references/readme-snippets.md` — badge/proof/demo/mermaid/attribution snippets.
- `assets/demo.svg`, `assets/logo.svg` — starting graphics to adapt.
- `evals/evals.json`, `LESSONS.md`, `scripts/read-lessons.mjs`.
