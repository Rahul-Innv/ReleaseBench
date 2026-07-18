# README showpiece snippets

Add only what is true. Order the top: logo → title → badges → pitch → proof → demo → what-it-is →
diagram → quick start.

## Badges (under the title)
Green only once the repo is public AND a CI run has passed. Replace `main` with the repo's default
branch if it isn't `main`.
```markdown
[![pipeline status](https://gitlab.com/OWNER/NAME/badges/main/pipeline.svg)](https://gitlab.com/OWNER/NAME/-/commits/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![node ≥18](https://img.shields.io/badge/node-%E2%89%A518-brightgreen.svg)](package.json)
```
GitHub CI badge: `https://github.com/OWNER/NAME/actions/workflows/<file>/badge.svg`.

## Proof / traction
```markdown
## Proven in the real world

<TOOL> has already run real, non-trivial work — e.g. <concrete outcome, scale/cost, when>.
```
Keep it honest; strip client names / personal figures unless the owner is fine sharing them.

## Demo
```markdown
## Demo

![<one-line caption of the flow>](demo.svg)

*<the flow in words: `cmd a` → `cmd b` → outcome>.*
```

## Architecture diagram (states the insight)
```markdown
```mermaid
flowchart LR
  A["entry / input"] --> B["core step"]
  B --> C{"decision?"}
  C -- yes --> D["outcome"]
```​
```

## Logo header
```markdown
<p align="center"><img src="logo.svg" alt="<NAME> logo" width="88"></p>
```

## Attribution + roadmap
- Real name in `LICENSE` (`Copyright (c) <year> <Real Name>`) and a `Built by <Name>.` line — a handle
  reads as less credible than a real founder.
- `ROADMAP.md`: state the deliberate current scope honestly (e.g. "Windows-first by design"), then
  near-term / later / non-goals. Trajectory matters for a portfolio/YC read.

## Honesty guardrails
Every badge, proof, and demo must be TRUE. The demo's commands/output must match what the tool actually
prints; use a GENERIC example, never the owner's private data.
